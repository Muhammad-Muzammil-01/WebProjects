# =============================================================================
# pages/4_Book_Appointment.py — Appointment Booking Page
# =============================================================================
# This is the most complex and important page in the app. It:
#   1. Renders a booking form (name, phone, email, service, barber, date, time)
#   2. Validates all inputs: presence check + phone regex + double-booking check
#   3. On valid submit: inserts the booking into SQLite and shows a summary
#
# Key concepts demonstrated here:
#   - Form validation without JavaScript (pure Python)
#   - Parameterized SQL queries to prevent injection
#   - Double-booking detection by querying the DB before inserting
#   - st.session_state for storing the booking result across reruns
#   - st.form() + st.form_submit_button() for Streamlit forms
# =============================================================================

import streamlit as st
import os
import sys
import re                # Python's built-in regular expressions module
from datetime import date, timedelta  # for setting min date on the date picker

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our data and database functions
from data     import SERVICES, BARBERS, TIME_SLOTS
from database import is_slot_taken, add_appointment

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Book Appointment | The Sharp Edge",
                   page_icon="📅", layout="wide")

# ── CSS injection ─────────────────────────────────────────────────────────────
def load_css():
    """Loads the global CSS stylesheet."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# ===========================================================================
# HELPER FUNCTIONS
# ===========================================================================

def validate_phone(phone_str: str) -> bool:
    """
    Validates a US-style phone number using a regular expression.

    Parameters:
        phone_str (str): The phone number string entered by the user.

    Returns:
        bool: True if the phone number matches a valid pattern, False otherwise.

    Accepted formats (all return True):
        - (718) 555-0199
        - 718-555-0199
        - 718.555.0199
        - 7185550199
        - +1 718 555 0199

    How the regex works (in plain English):
        Optionally matches a +1 country code, then an optional separator,
        then 3 area-code digits (optionally in parentheses), then a separator,
        then 3 exchange digits, then a separator, then 4 subscriber digits.
    """
    # The compiled regex pattern for US phone numbers
    pattern = r"^(\+1[\s\-.])?([\s\-.]?\(?\d{3}\)?[\s\-.]?\d{3}[\s\-.]?\d{4})$"

    # re.match checks if the pattern matches at the START of the string
    # We strip whitespace from both ends before checking
    return bool(re.match(pattern, phone_str.strip()))


def convert_24h_to_12h(time_24: str) -> str:
    """
    Converts a 24-hour time string to a 12-hour display string.

    Parameters:
        time_24 (str): Time in "HH:MM" format, e.g. "14:00"

    Returns:
        str: Time in "H:MM AM/PM" format, e.g. "2:00 PM"

    Used to make the time slot dropdown more user-friendly.
    """
    # Split "14:00" into hours=14 and minutes=00
    hour, minute = map(int, time_24.split(":"))

    # Determine AM or PM
    period = "AM" if hour < 12 else "PM"

    # Convert 24h to 12h: hour 0 → 12 AM, hour 13 → 1 PM, etc.
    display_hour = hour % 12 or 12   # modulo 12; "or 12" handles midnight (0 → 12)

    return f"{display_hour}:{minute:02d} {period}"   # ":02d" pads single-digit minutes


# ===========================================================================
# PAGE HEADER
# ===========================================================================

st.markdown(
    '<h1>📅 Book an Appointment</h1>'
    '<p style="color:#9a9a9a; font-size:1.05rem; margin-bottom:1.5rem;">'
    'Fill in your details below to reserve your spot. All fields are required.'
    '</p>'
    '<hr class="gold-divider">',
    unsafe_allow_html=True
)


# ===========================================================================
# SESSION STATE INITIALISATION
# ===========================================================================
# st.session_state is a dictionary that persists between Streamlit reruns
# (a "rerun" happens every time the user clicks anything).
# We use it to remember whether a booking was just successfully completed,
# so we can show the success card AFTER the form disappears.
#
# Without session_state, the app would forget the booking as soon as it
# re-renders — you'd lose the confirmation message.
# ===========================================================================

# Initialise the booking result key if it doesn't exist yet
if "last_booking" not in st.session_state:
    st.session_state["last_booking"] = None   # None means no booking made yet


# ===========================================================================
# SUCCESS CARD — shown after a successful booking
# ===========================================================================
# If a booking was just made, show the confirmation before the form.
# The user can then click "Book Another" to reset and show the form again.
# ===========================================================================

if st.session_state["last_booking"] is not None:
    booking = st.session_state["last_booking"]   # retrieve the saved booking dict

    # Build the confirmation HTML using the stored booking data
    success_html = (
        '<div class="success-box">'
        '<h3>✅ Booking Confirmed!</h3>'
        '<p style="color:#9a9a9a; margin-bottom:1rem;">We\'ll see you at The Sharp Edge. Here\'s your booking summary:</p>'
        '</div>'
        '<div class="booking-summary">'
        f'<p><span class="label">Ref #:</span> {booking["id"]}</p>'
        f'<p><span class="label">Name:</span> {booking["name"]}</p>'
        f'<p><span class="label">Service:</span> {booking["service"]}</p>'
        f'<p><span class="label">Barber:</span> {booking["barber"]}</p>'
        f'<p><span class="label">Date:</span> {booking["appt_date"]}</p>'
        f'<p><span class="label">Time:</span> {convert_24h_to_12h(booking["appt_time"])}</p>'
        f'<p><span class="label">Phone:</span> {booking["phone"]}</p>'
        f'<p><span class="label">Email:</span> {booking["email"]}</p>'
        '</div>'
    )
    st.markdown(success_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)   # vertical spacer

    # Button to book another appointment — clears the session state
    if st.button("🔄 Book Another Appointment"):
        st.session_state["last_booking"] = None   # clear the success state
        st.rerun()                                 # force Streamlit to re-render the form

    # Stop here — don't render the form while the success card is showing
    st.stop()


# ===========================================================================
# BOOKING FORM
# ===========================================================================
# st.form() groups all widgets into a single form with one submit button.
# None of the form widgets trigger a Streamlit rerun until the user clicks
# the submit button — this prevents partial-validation errors mid-typing.
# ===========================================================================

# Build dropdown options BEFORE the form so we can reference them
service_options = [s["name"] for s in SERVICES]     # ["Classic Haircut", "Beard Trim", ...]
barber_options  = [b["name"] for b in BARBERS]      # ["Marcus Reeves", "Jordan Lee", ...]

# Convert 24h time slots to 12h for display; keep 24h as the actual value
# The dropdown shows "2:00 PM" but we store "14:00" in the database
time_display_options = [convert_24h_to_12h(t) for t in TIME_SLOTS]
# Zip into a list of (display_label, stored_value) tuples
time_options_map = dict(zip(time_display_options, TIME_SLOTS))   # {"2:00 PM": "14:00", ...}

# Two-column layout: form on the left, tips panel on the right
form_col, tips_col = st.columns([3, 1])

with form_col:
    # st.form("booking_form") gives the form a unique key
    with st.form("booking_form", clear_on_submit=False):
        # ── Section: Personal Info ────────────────────────────────────────────
        st.markdown("#### 👤 Your Information")

        # Two sub-columns for name and phone on the same row
        name_col, phone_col = st.columns(2)

        with name_col:
            # st.text_input returns a string; placeholder shows hint text
            customer_name = st.text_input(
                "Full Name *",
                placeholder="e.g. John Smith",
                help="Enter your first and last name"
            )

        with phone_col:
            customer_phone = st.text_input(
                "Phone Number *",
                placeholder="e.g. (718) 555-0199",
                help="US format: (XXX) XXX-XXXX"
            )

        # Email on its own row (full width)
        customer_email = st.text_input(
            "Email Address *",
            placeholder="e.g. john.smith@email.com",
            help="We'll send your confirmation here"
        )

        st.markdown("---")   # native horizontal rule as a section separator

        # ── Section: Appointment Details ─────────────────────────────────────
        st.markdown("#### ✂️ Appointment Details")

        service_col, barber_col = st.columns(2)

        with service_col:
            # st.selectbox renders a dropdown; returns the selected string
            selected_service = st.selectbox(
                "Service *",
                options=service_options,
                help="See the Services page for pricing and duration"
            )

        with barber_col:
            selected_barber = st.selectbox(
                "Preferred Barber *",
                options=barber_options,
                help="Each barber has different specialties"
            )

        date_col, time_col = st.columns(2)

        with date_col:
            # st.date_input returns a Python date object
            # min_value prevents booking in the past; we allow today onwards
            selected_date = st.date_input(
                "Preferred Date *",
                min_value=date.today(),                  # can't book in the past
                max_value=date.today() + timedelta(days=60),  # max 60 days ahead
                value=date.today() + timedelta(days=1),  # default to tomorrow
                help="We're open Mon–Sun (see Home page for hours)"
            )

        with time_col:
            # st.selectbox for time slots — shows 12h display, maps to 24h value
            selected_time_display = st.selectbox(
                "Preferred Time *",
                options=time_display_options,
                help="Available slots in 30-minute increments"
            )

        st.markdown("---")

        # ── Notes field (optional) ────────────────────────────────────────────
        st.markdown("#### 📝 Additional Notes (Optional)")
        notes = st.text_area(
            "Anything we should know?",
            placeholder="e.g. First-time customer, allergies, specific style preferences...",
            height=80,
            label_visibility="collapsed"   # hides the label (we used markdown above)
        )

        # ── Submit Button ──────────────────────────────────────────────────────
        # st.form_submit_button only triggers a rerun when clicked
        submitted = st.form_submit_button(
            "📅 Confirm Booking",
            use_container_width=True,
            type="primary"    # renders with our CSS .stButton primary style
        )


# ===========================================================================
# FORM VALIDATION & SUBMISSION (runs only when the form is submitted)
# ===========================================================================
# All validation happens in Python, server-side.
# We collect all errors into a list so we can show ALL problems at once
# (better UX than showing one error at a time).
# ===========================================================================

    if submitted:
        # Collect all validation errors into this list
        errors = []

        # ── Presence checks — none of these can be empty ─────────────────
        if not customer_name.strip():
            errors.append("Full name is required.")

        if not customer_phone.strip():
            errors.append("Phone number is required.")

        if not customer_email.strip():
            errors.append("Email address is required.")

        # ── Phone format validation ────────────────────────────────────────
        # Only validate format if the field isn't empty (avoid duplicate errors)
        if customer_phone.strip() and not validate_phone(customer_phone):
            errors.append("Phone number format is invalid. Try: (718) 555-0199")

        # ── Email basic validation (must contain @ and a dot after @) ─────
        if customer_email.strip() and ("@" not in customer_email or "." not in customer_email.split("@")[-1]):
            errors.append("Email address doesn't look right. Check the format.")

        # ── Date must not be a Sunday — we're closed! ─────────────────────
        # .weekday() returns 0=Mon ... 6=Sun
        if selected_date.weekday() == 6:
            errors.append("We're closed on Sundays! Please choose another date.")

        # ── Convert the 24h time for DB storage ──────────────────────────
        # Look up the selected 12h display label in our map → get the 24h string
        selected_time_24h = time_options_map[selected_time_display]

        # Convert date object → string for SQLite (ISO 8601 format: YYYY-MM-DD)
        date_str = selected_date.strftime("%Y-%m-%d")

        # ── Friday midday break validation (closed 1:00 PM – 3:00 PM) ───
        # .weekday() returns 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
        if selected_date.weekday() == 4 and selected_time_24h in ["13:00", "13:30", "14:00", "14:30"]:
            errors.append(
                "The shop is closed on Fridays between 1:00 PM and 3:00 PM for the midday break. "
                "Please choose a slot before 1:00 PM or at/after 3:00 PM."
            )

        # ── Double-booking check ──────────────────────────────────────────
        # ONLY do the DB query if there are no other errors yet
        # (no point querying DB if the form is already invalid)
        if not errors:
            slot_conflict = is_slot_taken(selected_barber, date_str, selected_time_24h)
            if slot_conflict:
                # The barber is already booked at this exact date and time
                errors.append(
                    f"{selected_barber} is already booked at "
                    f"{selected_time_display} on {selected_date.strftime('%B %d, %Y')}. "
                    "Please choose a different time or barber."
                )

        # ── Show errors if any were found ─────────────────────────────────
        if errors:
            # st.error shows a red error box
            for error_msg in errors:
                st.error(f"⚠️ {error_msg}")   # one st.error per problem

        else:
            # ── ALL VALIDATIONS PASSED — insert into database ─────────────
            # add_appointment returns the new row's ID (for the confirmation)
            new_id = add_appointment(
                name      = customer_name.strip(),
                phone     = customer_phone.strip(),
                email     = customer_email.strip(),
                service   = selected_service,
                barber    = selected_barber,
                appt_date = date_str,
                appt_time = selected_time_24h,
            )

            # Store the booking details in session_state so the success card
            # can display them AFTER the page reruns
            st.session_state["last_booking"] = {
                "id":        new_id,
                "name":      customer_name.strip(),
                "phone":     customer_phone.strip(),
                "email":     customer_email.strip(),
                "service":   selected_service,
                "barber":    selected_barber,
                "appt_date": date_str,
                "appt_time": selected_time_24h,
            }

            # st.rerun() triggers Streamlit to re-execute this file from the top.
            # On the next run, session_state["last_booking"] is not None, so
            # the success card will render instead of the form.
            st.rerun()


# ── Tips Panel (right column) ─────────────────────────────────────────────────

with tips_col:
    tips_html = (
        '<div class="info-card">'
        '<div class="info-card-title">💡 Tips</div>'
        '<ul style="color:#9a9a9a; padding-left:1.2rem; font-size:0.88rem; line-height:2;">'
        '<li>Arrive 5 min early</li>'
        '<li>Bring a photo for reference styles</li>'
        '<li>Friday break: 1:00 – 3:00 PM</li>'
        '<li>Cancellations: 24hr notice</li>'
        '<li>Walk-ins also welcome</li>'
        '</ul>'
        '</div>'
        '<div class="info-card" style="margin-top:1rem;">'
        '<div class="info-card-title">⏱ Durations</div>'
        '<ul style="color:#9a9a9a; padding-left:1.2rem; font-size:0.88rem; line-height:2;">'
        '<li>Haircut: 30 min</li>'
        '<li>Beard Trim: 20 min</li>'
        '<li>Hot Shave: 40 min</li>'
        '<li>Combo: 50 min</li>'
        '</ul>'
        '</div>'
    )
    st.markdown(tips_html, unsafe_allow_html=True)
