# =============================================================================
# pages/5_Admin_Dashboard.py — Admin Dashboard Page
# =============================================================================
# A password-protected management panel that allows the shop owner to:
#   1. Log in with a simple password (stored in data.py / st.secrets)
#   2. View all bookings in a filterable table (st.dataframe)
#   3. Delete/cancel individual bookings by ID
#   4. See daily booking count metrics and a bar chart
#
# Authentication approach:
#   - A text_input(type="password") captures the password
#   - st.session_state["admin_logged_in"] stores the auth state
#   - This is a SIMPLE approach for a demo — explicitly NOT JWT/hashing
#   - In production you'd use st.secrets and a bcrypt-hashed password
#
# Key Streamlit concepts demonstrated:
#   - st.session_state for persistent auth state across reruns
#   - st.dataframe for read-only table display
#   - st.metric for KPI boxes
#   - st.bar_chart for quick visualisation
#   - Dynamic SQL filtering (date + barber filters)
# =============================================================================

import streamlit as st
import pandas as pd    # for converting dict list → DataFrame for st.dataframe
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data     import BARBERS, ADMIN_PASSWORD
from database import (
    get_all_appointments,
    get_appointments_filtered,
    delete_appointment,
    get_booking_counts_by_day,
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Admin Dashboard | The Sharp Edge",
                   page_icon="🔒", layout="wide")

# ── CSS injection ─────────────────────────────────────────────────────────────
def load_css():
    """Loads the global CSS stylesheet."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# ===========================================================================
# SESSION STATE: AUTH INITIALISATION
# ===========================================================================
# We store the admin login state in session_state so the user stays logged
# in as they interact with the page (each widget click reruns the script,
# so without session_state the login check would reset constantly).
# ===========================================================================

# Initialise auth flag to False if it hasn't been set this session
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False   # default: not logged in


# ===========================================================================
# LOGIN SCREEN — shown when not authenticated
# ===========================================================================

if not st.session_state["admin_logged_in"]:

    # Center the login form using column spacers
    _, login_col, _ = st.columns([2, 3, 2])

    with login_col:
        st.markdown("""
            <div style='text-align:center; padding:3rem 0 1.5rem;'>
                <div style='font-size:3rem;'>🔒</div>
                <h2 style='color:#c9a84c;'>Admin Login</h2>
                <p style='color:#9a9a9a;'>
                    This area is restricted to shop staff only.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Password input: type="password" masks characters as user types
        # The value is NOT stored in session_state automatically — we read it here
        password_input = st.text_input(
            "Admin Password",
            type="password",        # masks the input characters
            placeholder="Enter admin password",
            label_visibility="hidden"
        )

        # Login button
        if st.button("🔓 Login", use_container_width=True):
            # Compare entered password to the one in data.py
            # In production: use st.secrets["admin_password"] instead of data.py
            if password_input == ADMIN_PASSWORD:
                # Set the flag to True — all subsequent reruns will skip this block
                st.session_state["admin_logged_in"] = True
                st.success("✅ Login successful! Loading dashboard...")
                st.rerun()   # rerun to render the dashboard immediately
            else:
                # Wrong password — show error, keep on login screen
                st.error("❌ Incorrect password. Please try again.")

    # Stop rendering — don't show anything else while logged out
    st.stop()


# ===========================================================================
# ADMIN DASHBOARD — only reaches here if logged in
# ===========================================================================

# ── Dashboard Header ──────────────────────────────────────────────────────────
col_title, col_logout = st.columns([5, 1])

with col_title:
    st.markdown("""
        <div class="admin-header">
            <h1 style="margin:0; font-size:1.8rem;">🔒 Admin Dashboard</h1>
            <p style="color:#9a9a9a; margin:0.3rem 0 0; font-size:0.9rem;">
                The Sharp Edge Barber Shop — Booking Management
            </p>
        </div>
    """, unsafe_allow_html=True)

with col_logout:
    st.markdown("<br>", unsafe_allow_html=True)   # push button down
    if st.button("🚪 Log Out", use_container_width=True):
        # Clear the auth flag → on rerun, the login screen shows again
        st.session_state["admin_logged_in"] = False
        st.rerun()

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)


# ===========================================================================
# SECTION 1: KPI METRICS
# ===========================================================================
# Load all bookings once and compute stats from them in Python.
# We do ONE db query here and reuse the data everywhere on the page.
# ===========================================================================

all_bookings = get_all_appointments()   # list of dicts, newest first

# Compute metrics from the raw list
total_bookings = len(all_bookings)

# Count bookings with today's date
from datetime import date
today_str = date.today().strftime("%Y-%m-%d")    # "2024-09-15"
todays_bookings = sum(1 for b in all_bookings if b["appt_date"] == today_str)

# Most booked barber (if any bookings exist)
if all_bookings:
    # Count occurrences of each barber name
    barber_counts = {}
    for b in all_bookings:
        barber_counts[b["barber"]] = barber_counts.get(b["barber"], 0) + 1
    # max() with key= selects the barber with the highest count
    top_barber = max(barber_counts, key=barber_counts.get)
    top_barber_display = f"{top_barber} ({barber_counts[top_barber]})"
else:
    top_barber_display = "N/A"

# Display the three metric boxes side by side
m1, m2, m3 = st.columns(3)

with m1:
    # st.metric(label, value) renders a styled KPI box
    st.metric("📋 Total Bookings", total_bookings)

with m2:
    st.metric("📅 Today's Bookings", todays_bookings)

with m3:
    st.metric("⭐ Most Booked Barber", top_barber_display)

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)


# ===========================================================================
# SECTION 2: BOOKINGS CHART
# ===========================================================================
# Show a bar chart of bookings per day using st.bar_chart.
# Data comes from get_booking_counts_by_day() which uses SQL GROUP BY.
# ===========================================================================

st.markdown("<h2>📊 Bookings by Day</h2>", unsafe_allow_html=True)

counts_by_day = get_booking_counts_by_day()   # dict: {"2024-09-15": 3, ...}

if counts_by_day:
    # Convert the dict to a pandas DataFrame — st.bar_chart needs a DataFrame
    chart_df = pd.DataFrame(
        list(counts_by_day.items()),    # list of (date, count) tuples
        columns=["Date", "Bookings"]   # column names
    )
    chart_df = chart_df.set_index("Date")   # Date becomes the x-axis labels

    # st.bar_chart takes a DataFrame; the index becomes x-axis, values become bars
    st.bar_chart(chart_df, use_container_width=True, height=250)
else:
    # Friendly message when there's no data yet
    st.info("📭 No booking data yet. The chart will appear once appointments are made.")

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)


# ===========================================================================
# SECTION 3: FILTERS
# ===========================================================================
# Two filter dropdowns: one for date, one for barber.
# Filters are applied together (AND logic) via get_appointments_filtered().
# ===========================================================================

st.markdown("<h2>📋 All Bookings</h2>", unsafe_allow_html=True)

filter_col1, filter_col2, filter_col3 = st.columns([2, 2, 1])

with filter_col1:
    # Date filter: text input for manual date entry (YYYY-MM-DD)
    # We use text instead of date_input so "All dates" is an option (empty string)
    date_filter_input = st.text_input(
        "🔍 Filter by Date",
        placeholder="YYYY-MM-DD or leave empty for all",
        help="Example: 2024-09-15"
    )

with filter_col2:
    # Barber filter: dropdown with "All" as the first option
    barber_names = ["All"] + [b["name"] for b in BARBERS]   # prepend "All"
    barber_filter_input = st.selectbox(
        "🔍 Filter by Barber",
        options=barber_names
    )

with filter_col3:
    st.markdown("<br>", unsafe_allow_html=True)   # align button with inputs
    if st.button("🔄 Reset Filters", use_container_width=True):
        # Streamlit doesn't have a native "clear input" function;
        # we use st.rerun() which resets all widget states to their defaults
        st.rerun()


# Fetch bookings with the filters applied
# Pass None for date if the input is empty (function handles None as "no filter")
date_filter_value  = date_filter_input.strip() if date_filter_input.strip() else None
barber_filter_value = barber_filter_input    # "All" is handled inside the function

filtered_bookings = get_appointments_filtered(
    date_filter   = date_filter_value,
    barber_filter = barber_filter_value,
)


# ===========================================================================
# SECTION 4: BOOKINGS TABLE
# ===========================================================================

if filtered_bookings:
    # Convert list of dicts to a pandas DataFrame for clean display
    df = pd.DataFrame(filtered_bookings)

    # Rename columns to be more human-readable in the table
    df = df.rename(columns={
        "id":         "ID",
        "name":       "Customer",
        "phone":      "Phone",
        "email":      "Email",
        "service":    "Service",
        "barber":     "Barber",
        "appt_date":  "Date",
        "appt_time":  "Time",
        "created_at": "Booked At",
    })

    # Display the DataFrame as a read-only interactive table
    # hide_index=True removes the 0,1,2... row numbers
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Show how many results the filter returned
    st.markdown(f"<p class='muted'>Showing {len(filtered_bookings)} booking(s)</p>",
                unsafe_allow_html=True)

else:
    st.info("📭 No bookings found matching your filters.")


# ===========================================================================
# SECTION 5: DELETE / CANCEL A BOOKING
# ===========================================================================
# The admin enters a booking ID (from the table above) and clicks Delete.
# We show a confirmation step using a checkbox to prevent accidental deletes.
# ===========================================================================

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
st.markdown("<h2>🗑️ Cancel a Booking</h2>", unsafe_allow_html=True)

if all_bookings:
    # Get all valid IDs from the current bookings
    valid_ids = [b["id"] for b in all_bookings]

    del_col1, del_col2 = st.columns([2, 3])

    with del_col1:
        # Number input for the booking ID to delete
        delete_id = st.number_input(
            "Enter Booking ID to Cancel",
            min_value=1,         # IDs start at 1 (auto-increment)
            step=1,              # whole numbers only
            format="%d",         # display as integer (no decimal)
            help="Find the ID in the bookings table above"
        )

    with del_col2:
        st.markdown("<br>", unsafe_allow_html=True)

        # Confirm checkbox — prevents accidental deletion
        confirm_delete = st.checkbox(
            f"✅ I confirm I want to cancel Booking #{int(delete_id)}",
            value=False   # unchecked by default
        )

        # Delete button — only enabled after checkbox is checked
        if st.button("🗑️ Cancel Booking", type="primary",
                     disabled=not confirm_delete):   # button is greyed out if not confirmed

            # Verify the ID actually exists in the database
            if int(delete_id) in valid_ids:
                delete_appointment(int(delete_id))    # DB delete call
                st.success(f"✅ Booking #{int(delete_id)} has been cancelled.")
                # Rerun to refresh the table — the deleted row will no longer appear
                st.rerun()
            else:
                st.error(f"⚠️ Booking ID #{int(delete_id)} not found.")
else:
    st.info("📭 No bookings to cancel yet.")

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)


# ===========================================================================
# SECTION 6: CONTACT FORM MESSAGES (bonus admin view)
# ===========================================================================
# Show any messages submitted via the Contact page.
# Uses a direct SQL query via get_connection (simple, no separate function needed).
# ===========================================================================

st.markdown("<h2>✉️ Contact Form Messages</h2>", unsafe_allow_html=True)

# Import get_connection so we can run a quick query inline
from database import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages ORDER BY id DESC")
    messages = [dict(row) for row in cursor.fetchall()]
    conn.close()

    if messages:
        msg_df = pd.DataFrame(messages).rename(columns={
            "id":          "ID",
            "sender_name": "Name",
            "message":     "Message",
            "sent_at":     "Sent At",
        })
        st.dataframe(msg_df, use_container_width=True, hide_index=True)
    else:
        st.info("📭 No contact messages yet.")

except Exception as e:
    # Graceful error display — the messages table might not exist on very first run
    st.warning(f"Could not load messages: {e}")
