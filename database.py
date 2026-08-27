# =============================================================================
# database.py — All SQLite database operations for the Barber Shop app
# =============================================================================
# This module is the ONLY place that talks to the database.
# Every other file imports functions from here — this is the "data layer."
#
# DATABASE SCHEMA OVERVIEW
# ─────────────────────────
# Table: appointments
#   id          INTEGER  PRIMARY KEY AUTOINCREMENT  — unique row identifier
#   name        TEXT     NOT NULL  — customer's full name
#   phone       TEXT     NOT NULL  — customer's phone number
#   email       TEXT     NOT NULL  — customer's email address
#   service     TEXT     NOT NULL  — service chosen (matches SERVICES[n]["name"])
#   barber      TEXT     NOT NULL  — barber chosen (matches BARBERS[n]["name"])
#   appt_date   TEXT     NOT NULL  — date in YYYY-MM-DD format (ISO 8601)
#   appt_time   TEXT     NOT NULL  — time in HH:MM 24-hour format
#   created_at  TEXT     NOT NULL  — timestamp when the booking was submitted
#
# Table: messages
#   id          INTEGER  PRIMARY KEY AUTOINCREMENT
#   sender_name TEXT     NOT NULL  — name from the contact form
#   message     TEXT     NOT NULL  — message body
#   sent_at     TEXT     NOT NULL  — timestamp of submission
#
# WHY NO FOREIGN KEYS?
#   SQLite supports foreign keys but they must be enabled per-connection with
#   PRAGMA foreign_keys = ON. For a junior demo app, keeping everything as TEXT
#   is simpler to explain. In a real app, barbers and services would be their
#   own tables with INTEGER foreign keys for data integrity.
#
# SQL INJECTION PREVENTION
#   Every query uses "?" placeholders and passes values as a tuple.
#   The sqlite3 driver escapes the values automatically before they hit the DB.
#   NEVER build queries with f-strings or % formatting — a malicious input like
#   "'; DROP TABLE appointments; --" would execute if you did.
# =============================================================================

import sqlite3                    # built-in Python module — no pip install needed
import os                         # used to build a safe file path
from datetime import datetime     # used to generate timestamps

# ---------------------------------------------------------------------------
# DATABASE FILE PATH
# We store barber_shop.db next to this file so it works locally AND on
# Streamlit Community Cloud (which gives us a writable /tmp or project dir).
# ---------------------------------------------------------------------------
# os.path.dirname(__file__) → folder where database.py lives
# os.path.join builds the correct path for the current OS
DB_PATH = os.path.join(os.path.dirname(__file__), "barber_shop.db")


# ===========================================================================
# FUNCTION: get_connection
# ===========================================================================
def get_connection():
    """
    Opens and returns a connection to the SQLite database.

    Returns:
        sqlite3.Connection: An active connection object.

    Why a function?
        Every DB operation opens its own connection and closes it when done.
        This avoids "database is locked" errors that happen when a single
        long-lived connection is shared across Streamlit reruns.

    Why check_same_thread=False?
        Streamlit can run callback functions on different threads.
        SQLite connections are not thread-safe by default; this flag tells
        sqlite3 to allow it (safe for our single-user app).
    """
    # sqlite3.connect creates the file if it doesn't exist
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)

    # row_factory makes each row behave like a dict (column name → value)
    # so we can write row["name"] instead of row[0]
    connection.row_factory = sqlite3.Row

    return connection   # caller is responsible for calling .close()


# ===========================================================================
# FUNCTION: init_db
# ===========================================================================
def init_db():
    """
    Creates the database tables if they don't already exist.

    Parameters: None
    Returns:    None

    Why 'CREATE TABLE IF NOT EXISTS'?
        This is idempotent — safe to call every time the app starts.
        If the table exists, the command does nothing. If it doesn't, it
        creates it. This means we don't need a separate migration step.

    Call this once in app.py before any page is shown.
    """
    conn = get_connection()     # open a connection

    # cursor() gives us an object we use to run SQL statements
    cursor = conn.cursor()

    # -----------------------------------------------------------------------
    # CREATE TABLE: appointments
    # -----------------------------------------------------------------------
    # Each column definition: name  TYPE  CONSTRAINT
    # TEXT is used for dates/times because SQLite has no native DATE type;
    # storing as ISO strings still sorts correctly (YYYY-MM-DD > YYYY-MM-DD).
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            phone       TEXT    NOT NULL,
            email       TEXT    NOT NULL,
            service     TEXT    NOT NULL,
            barber      TEXT    NOT NULL,
            appt_date   TEXT    NOT NULL,
            appt_time   TEXT    NOT NULL,
            created_at  TEXT    NOT NULL
        )
    """)

    # -----------------------------------------------------------------------
    # CREATE TABLE: messages  (contact form submissions)
    # -----------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_name TEXT    NOT NULL,
            message     TEXT    NOT NULL,
            sent_at     TEXT    NOT NULL
        )
    """)

    conn.commit()   # write the schema changes to disk
    conn.close()    # always close the connection when done


# ===========================================================================
# FUNCTION: is_slot_taken
# ===========================================================================
def is_slot_taken(barber: str, appt_date: str, appt_time: str) -> bool:
    """
    Checks whether a barber already has a booking at the given date and time.

    Parameters:
        barber    (str): Barber name, e.g. "Marcus Reeves"
        appt_date (str): Date in YYYY-MM-DD format, e.g. "2024-09-15"
        appt_time (str): Time in HH:MM format, e.g. "14:00"

    Returns:
        bool: True if the slot is already booked, False if it's available.

    How it works:
        SELECT COUNT(*) counts rows matching the three conditions.
        If count > 0, the slot is taken. This is the double-booking check.
        Using parameterized queries ("?") prevents SQL injection.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # The three "?" placeholders are replaced safely by the tuple (barber, ...)
    # sqlite3 escapes special characters so a malicious string can't break out
    cursor.execute("""
        SELECT COUNT(*)
        FROM   appointments
        WHERE  barber    = ?
          AND  appt_date = ?
          AND  appt_time = ?
    """, (barber, appt_date, appt_time))    # values passed as a tuple, not in the string

    count = cursor.fetchone()[0]    # fetchone() returns the first (only) row; [0] = COUNT
    conn.close()

    return count > 0    # True → conflict exists; False → slot is free


# ===========================================================================
# FUNCTION: add_appointment
# ===========================================================================
def add_appointment(name: str, phone: str, email: str,
                    service: str, barber: str,
                    appt_date: str, appt_time: str) -> int:
    """
    Inserts a new appointment into the appointments table.

    Parameters:
        name      (str): Customer's full name
        phone     (str): Customer's phone number
        email     (str): Customer's email
        service   (str): Service name (e.g. "Classic Haircut")
        barber    (str): Barber name (e.g. "Marcus Reeves")
        appt_date (str): Date in YYYY-MM-DD format
        appt_time (str): Time in HH:MM 24-hour format

    Returns:
        int: The auto-generated ID of the newly created appointment row.
             Useful for showing the customer their booking reference number.

    Why return lastrowid?
        After INSERT, cursor.lastrowid gives us the new row's primary key.
        We can display this as a "booking reference" in the success message.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # datetime.now().isoformat() gives "2024-09-15T14:32:01.123456" — a
    # sortable, human-readable timestamp stored as TEXT in SQLite
    created_at = datetime.now().isoformat(timespec="seconds")

    # Eight "?" placeholders match the eight values in the tuple exactly
    cursor.execute("""
        INSERT INTO appointments
            (name, phone, email, service, barber, appt_date, appt_time, created_at)
        VALUES
            (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, phone, email, service, barber, appt_date, appt_time, created_at))

    conn.commit()                       # persist the INSERT to disk
    new_id = cursor.lastrowid           # capture the auto-generated primary key
    conn.close()

    return new_id   # returned so the booking page can show "Booking Ref #7"


# ===========================================================================
# FUNCTION: get_all_appointments
# ===========================================================================
def get_all_appointments() -> list[dict]:
    """
    Fetches every row from the appointments table, newest first.

    Parameters: None

    Returns:
        list[dict]: A list of appointment dicts. Each dict has keys matching
                    the column names (id, name, phone, email, service, barber,
                    appt_date, appt_time, created_at).
                    Returns an empty list if there are no appointments.

    Why ORDER BY id DESC?
        Shows the most recent bookings at the top of the admin dashboard,
        which is more useful than chronological insertion order.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM appointments ORDER BY id DESC")

    # fetchall() returns a list of sqlite3.Row objects.
    # dict(row) converts each Row into a plain Python dict — easier to work
    # with in Streamlit (e.g. passing to pandas DataFrame).
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return rows     # empty list [] if the table has no rows


# ===========================================================================
# FUNCTION: get_appointments_filtered
# ===========================================================================
def get_appointments_filtered(date_filter: str = None, barber_filter: str = None) -> list[dict]:
    """
    Fetches appointments, optionally filtered by date and/or barber.

    Parameters:
        date_filter   (str | None): If provided, only return rows where
                                    appt_date = this value (YYYY-MM-DD).
        barber_filter (str | None): If provided, only return rows where
                                    barber = this name.

    Returns:
        list[dict]: Filtered list of appointment dicts, newest first.

    How it works:
        We build the WHERE clause dynamically by appending conditions and
        values to lists, then join them. This avoids duplicate query strings
        and still uses parameterized placeholders — no SQL injection risk.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Start with the base query; conditions and values will be appended
    query = "SELECT * FROM appointments"
    conditions = []     # list of "column = ?" strings
    values = []         # matching list of actual values

    # Only add a condition if the filter was actually provided (not None)
    if date_filter:
        conditions.append("appt_date = ?")  # placeholder, not the value
        values.append(date_filter)           # value goes in the list

    if barber_filter and barber_filter != "All":
        conditions.append("barber = ?")
        values.append(barber_filter)

    # If there are any conditions, join them with AND and append to query
    if conditions:
        query += " WHERE " + " AND ".join(conditions)   # e.g. "WHERE appt_date = ? AND barber = ?"

    query += " ORDER BY appt_date ASC, appt_time ASC"   # chronological within filters

    cursor.execute(query, values)   # values list acts as the tuple of "?" replacements
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return rows


# ===========================================================================
# FUNCTION: delete_appointment
# ===========================================================================
def delete_appointment(appointment_id: int) -> None:
    """
    Deletes a single appointment row by its primary key ID.

    Parameters:
        appointment_id (int): The ID of the row to delete.

    Returns: None

    Why delete by ID?
        The ID is unique (PRIMARY KEY), so there's no risk of accidentally
        deleting the wrong row. The admin sees IDs in the dashboard table
        and selects which one to remove.

    Security note:
        Even here, we use a "?" placeholder so a crafted integer-looking
        string can't inject SQL.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # "?" means the value of appointment_id is passed safely, not embedded
    cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
    # Note the trailing comma in (appointment_id,) — this makes it a tuple,
    # which is what sqlite3 requires even for a single value.

    conn.commit()   # persist the DELETE
    conn.close()


# ===========================================================================
# FUNCTION: get_booking_counts_by_day
# ===========================================================================
def get_booking_counts_by_day() -> dict:
    """
    Returns a dictionary of {date_string: booking_count} for all dates
    that have at least one appointment. Used to render the bar chart in
    the admin dashboard.

    Parameters: None

    Returns:
        dict: Keys are date strings (YYYY-MM-DD), values are integer counts.
              e.g. {"2024-09-15": 3, "2024-09-16": 1}
              Returns an empty dict if no appointments exist.

    Why GROUP BY?
        Instead of fetching all rows and counting in Python, we let SQL do
        the aggregation — it's faster and uses less memory for large datasets.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT   appt_date,
                 COUNT(*) AS booking_count    -- COUNT(*) tallies rows per group
        FROM     appointments
        GROUP BY appt_date                    -- one row per unique date
        ORDER BY appt_date ASC               -- chronological order for the chart
    """)

    # Build a dict from the result rows: {date: count}
    counts = {row["appt_date"]: row["booking_count"] for row in cursor.fetchall()}
    conn.close()

    return counts


# ===========================================================================
# FUNCTION: add_message
# ===========================================================================
def add_message(sender_name: str, message: str) -> None:
    """
    Saves a contact form submission to the messages table.

    Parameters:
        sender_name (str): The name the visitor entered in the contact form.
        message     (str): The message body they typed.

    Returns: None

    Why store messages in SQLite?
        It demonstrates full CRUD even on the contact page and gives the shop
        owner a way to review inquiries from the admin panel in a future iteration.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Capture when the message was sent
    sent_at = datetime.now().isoformat(timespec="seconds")

    cursor.execute("""
        INSERT INTO messages (sender_name, message, sent_at)
        VALUES (?, ?, ?)
    """, (sender_name, message, sent_at))

    conn.commit()
    conn.close()
