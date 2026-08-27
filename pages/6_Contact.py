# =============================================================================
# pages/6_Contact.py — Contact Page
# =============================================================================
# Provides two things:
#   1. Styled shop contact info (address, phone, email, hours)
#   2. A working contact form that saves messages to the SQLite 'messages' table
#
# The form demonstrates:
#   - Basic form validation (no empty fields)
#   - Database INSERT via the add_message() function in database.py
#   - st.session_state for form submission confirmation (same pattern as booking)
# =============================================================================

import streamlit as st
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data     import SHOP_INFO
from database import add_message   # function to save contact form to SQLite

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Contact | The Sharp Edge", page_icon="✉️", layout="wide")

# ── CSS injection ─────────────────────────────────────────────────────────────
def load_css():
    """Loads the global CSS stylesheet."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# ── Page header ──────────────────────────────────────────────────────────────
st.markdown("""
    <h1>✉️ Contact Us</h1>
    <p style='color:#9a9a9a; font-size:1.05rem; margin-bottom:2rem;'>
        Have a question? Want to book a group event? Just say hi.
        Fill in the form or reach us directly using the info below.
    </p>
    <hr class="gold-divider">
""", unsafe_allow_html=True)


# ===========================================================================
# TWO-COLUMN LAYOUT: Left = Contact Info, Right = Contact Form
# ===========================================================================

info_col, form_col = st.columns([1, 1])


# ── LEFT: Contact Information ─────────────────────────────────────────────────

with info_col:
    st.markdown("<h2>📍 Our Details</h2>", unsafe_allow_html=True)

    # Main contact card
    contact_info_html = f"""
        <div class="contact-card">
            <!-- Address row -->
            <div class="contact-item">
                <span class="contact-icon">🗺️</span>
                <div>
                    <strong style="color:#c9a84c;">Address</strong><br>
                    <span>{SHOP_INFO['address']}</span>
                </div>
            </div>

            <hr style="border-color:#2e2e2e; margin:0.8rem 0;">

            <!-- Phone row -->
            <div class="contact-item">
                <span class="contact-icon">📞</span>
                <div>
                    <strong style="color:#c9a84c;">Phone</strong><br>
                    <span>{SHOP_INFO['phone']}</span>
                </div>
            </div>

            <hr style="border-color:#2e2e2e; margin:0.8rem 0;">

            <!-- Email row -->
            <div class="contact-item">
                <span class="contact-icon">✉️</span>
                <div>
                    <strong style="color:#c9a84c;">Email</strong><br>
                    <span>{SHOP_INFO['email']}</span>
                </div>
            </div>
        </div>
    """
    st.markdown(contact_info_html, unsafe_allow_html=True)

    # Opening hours summary card
    hours_items = "".join([
        f'<div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #2e2e2e;"><span style="color:#9a9a9a;">{day}</span><span style="color:#f5f5f5; font-weight:600;">{hours}</span></div>'
        for day, hours in SHOP_INFO["hours"]
    ])
    hours_html = f'<div class="contact-card"><div class="info-card-title">🕐 Opening Hours</div>{hours_items}</div>'
    st.markdown(hours_html, unsafe_allow_html=True)

    # Social media / other links (static, no real links needed for demo)
    st.markdown("""
        <div class="contact-card" style="margin-top:1rem;">
            <div class="info-card-title">📱 Follow Us</div>
            <div style="display:flex; gap:1rem; margin-top:0.5rem;">
                <span style="color:#9a9a9a;">📸 @thesharpedge.bk</span>
                <span style="color:#9a9a9a;">|</span>
                <span style="color:#9a9a9a;">🐦 @SharpEdgeBK</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ── RIGHT: Contact Form ───────────────────────────────────────────────────────

with form_col:
    st.markdown("<h2>💬 Send Us a Message</h2>", unsafe_allow_html=True)

    # ===========================================================================
    # Session state for message submission confirmation
    # ===========================================================================
    # Same pattern as the booking page:
    # "message_sent" is False until the form submits successfully.
    # After success, we show a thank-you card instead of the form.
    # ===========================================================================

    if "message_sent" not in st.session_state:
        st.session_state["message_sent"] = False   # default state

    # If message was just sent, show confirmation and offer to send another
    if st.session_state["message_sent"]:
        st.markdown("""
            <div class="success-box">
                <h3>✅ Message Received!</h3>
                <p style="color:#9a9a9a;">
                    Thanks for reaching out! We'll get back to you within 24 hours.
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Reset button — sets flag back to False, reruns to show the form again
        if st.button("✉️ Send Another Message"):
            st.session_state["message_sent"] = False
            st.rerun()

    else:
        # ── Show the contact form ─────────────────────────────────────────────
        with st.form("contact_form", clear_on_submit=True):
            # Name field
            sender_name = st.text_input(
                "Your Name *",
                placeholder="e.g. John Smith",
            )

            # Email (optional — we don't store it in this simple version)
            sender_email = st.text_input(
                "Your Email (optional)",
                placeholder="e.g. john@email.com",
            )

            # Subject line
            subject = st.text_input(
                "Subject",
                placeholder="e.g. Group booking enquiry",
            )

            # Main message body
            message_body = st.text_area(
                "Your Message *",
                placeholder="Type your message here...",
                height=150,
            )

            # Submit button for the contact form
            send_submitted = st.form_submit_button(
                "📨 Send Message",
                use_container_width=True,
                type="primary"
            )

        # ── Validation and submission (outside the form block) ────────────────
        if send_submitted:
            contact_errors = []

            # Check that required fields are not empty
            if not sender_name.strip():
                contact_errors.append("Please enter your name.")
            if not message_body.strip():
                contact_errors.append("Message cannot be empty.")

            # Optional: basic email format check if email was provided
            if sender_email.strip() and "@" not in sender_email:
                contact_errors.append("Email address doesn't look right.")

            if contact_errors:
                # Show all errors
                for err in contact_errors:
                    st.error(f"⚠️ {err}")
            else:
                # Build the full message to save (include subject if provided)
                full_message = message_body.strip()
                if subject.strip():
                    # Prepend the subject line to the message for admin readability
                    full_message = f"[Subject: {subject.strip()}]\n\n{full_message}"

                # Save to the messages table in SQLite
                add_message(
                    sender_name = sender_name.strip(),
                    message     = full_message,
                )

                # Set the confirmation flag → rerun will show the success card
                st.session_state["message_sent"] = True
                st.rerun()


# ===========================================================================
# EMBEDDED MAP PLACEHOLDER
# ===========================================================================
# In a real app you'd embed a Google Maps iframe here.
# For this demo, we show a styled placeholder card.
# (Google Maps embed requires an API key which we're avoiding.)
# ===========================================================================

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

st.markdown("""
    <div class="contact-card" style="text-align:center; padding:3rem;">
        <div style="font-size:3rem; margin-bottom:1rem;">🗺️</div>
        <div class="info-card-title">Find Us on the Map</div>
        <p style="color:#9a9a9a;">
            124 Main Street, Brooklyn, NY 11201<br>
            <em style="font-size:0.85rem;">
                (Nearest subway: Jay St–MetroTech — A, C, F trains)
            </em>
        </p>
        <p style="color:#9a9a9a; font-size:0.85rem; margin-top:1rem;">
            💡 In production: replace this card with an embedded Google Maps iframe
            using your API key from Google Cloud Console.
        </p>
    </div>
""", unsafe_allow_html=True)
