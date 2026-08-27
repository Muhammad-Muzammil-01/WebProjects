# =============================================================================
# pages/6_Contact.py — Contact Page
# =============================================================================
import streamlit as st
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import SHOP_INFO
from database import add_message

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Contact | The Sharp Edge", page_icon="✉️", layout="wide")

# ── CSS injection ─────────────────────────────────────────────────────────────
def load_css():
    """Loads the global CSS stylesheet."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>\n{f.read()}\n</style>", unsafe_allow_html=True)

load_css()

# ── Page header ──────────────────────────────────────────────────────────────
st.markdown(
    '<h1>✉️ Contact Us</h1>'
    '<p style="color:#9a9a9a; font-size:1.05rem; margin-bottom:2rem;">'
    'Have a question? Want to book a group event? Just say hi. Fill in the form or reach us directly using the info below.'
    '</p>'
    '<hr class="gold-divider">',
    unsafe_allow_html=True
)

# ===========================================================================
# TWO-COLUMN LAYOUT: Left = Contact Info, Right = Contact Form
# ===========================================================================
info_col, form_col = st.columns([1, 1])

# ── LEFT: Contact Information ─────────────────────────────────────────────────
with info_col:
    st.markdown("<h2>📍 Our Details</h2>", unsafe_allow_html=True)

    # Main contact card
    contact_info_html = (
        '<div class="contact-card">'
        '<div class="contact-item">'
        '<span class="contact-icon">🗺️</span>'
        f'<div><strong style="color:#c9a84c;">Address</strong><br><span>{SHOP_INFO["address"]}</span></div>'
        '</div>'
        '<hr style="border-color:#2e2e2e; margin:0.8rem 0;">'
        '<div class="contact-item">'
        '<span class="contact-icon">📞</span>'
        f'<div><strong style="color:#c9a84c;">Phone</strong><br><span>{SHOP_INFO["phone"]}</span></div>'
        '</div>'
        '<hr style="border-color:#2e2e2e; margin:0.8rem 0;">'
        '<div class="contact-item">'
        '<span class="contact-icon">✉️</span>'
        f'<div><strong style="color:#c9a84c;">Email</strong><br><span>{SHOP_INFO["email"]}</span></div>'
        '</div>'
        '</div>'
    )
    st.markdown(contact_info_html, unsafe_allow_html=True)

    # Opening hours summary card
    hours_items = "".join([
        f'<div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid #2e2e2e;"><span style="color:#9a9a9a;">{day}</span><span style="color:#f5f5f5; font-weight:600;">{hours}</span></div>'
        for day, hours in SHOP_INFO["hours"]
    ])
    hours_html = f'<div class="contact-card"><div class="info-card-title">🕐 Opening Hours</div>{hours_items}</div>'
    st.markdown(hours_html, unsafe_allow_html=True)

    # Social media
    social_html = (
        '<div class="contact-card" style="margin-top:1rem;">'
        '<div class="info-card-title">📱 Follow Us</div>'
        '<div style="display:flex; gap:1rem; margin-top:0.5rem;">'
        '<span style="color:#9a9a9a;">📸 @thesharpedge.bk</span>'
        '<span style="color:#9a9a9a;">|</span>'
        '<span style="color:#9a9a9a;">🐦 @SharpEdgeBK</span>'
        '</div>'
        '</div>'
    )
    st.markdown(social_html, unsafe_allow_html=True)

# ── RIGHT: Contact Form ───────────────────────────────────────────────────────
with form_col:
    st.markdown("<h2>💬 Send Us a Message</h2>", unsafe_allow_html=True)

    if "message_sent" not in st.session_state:
        st.session_state["message_sent"] = False

    if st.session_state["message_sent"]:
        st.markdown(
            '<div class="success-box">'
            '<h3>✅ Message Received!</h3>'
            '<p style="color:#9a9a9a;">Thanks for reaching out! We\'ll get back to you within 24 hours.</p>'
            '</div>',
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✉️ Send Another Message"):
            st.session_state["message_sent"] = False
            st.rerun()

    else:
        with st.form("contact_form", clear_on_submit=True):
            sender_name = st.text_input("Your Name *", placeholder="e.g. John Smith")
            sender_email = st.text_input("Your Email (optional)", placeholder="e.g. john@email.com")
            subject = st.text_input("Subject", placeholder="e.g. Group booking enquiry")
            message_body = st.text_area("Your Message *", placeholder="Type your message here...", height=150)
            send_submitted = st.form_submit_button("📨 Send Message", use_container_width=True, type="primary")

        if send_submitted:
            contact_errors = []
            if not sender_name.strip():
                contact_errors.append("Please enter your name.")
            if not message_body.strip():
                contact_errors.append("Message cannot be empty.")
            if sender_email.strip() and "@" not in sender_email:
                contact_errors.append("Email address doesn't look right.")

            if contact_errors:
                for err in contact_errors:
                    st.error(f"⚠️ {err}")
            else:
                full_message = message_body.strip()
                if subject.strip():
                    full_message = f"[Subject: {subject.strip()}]\n\n{full_message}"

                add_message(
                    sender_name=sender_name.strip(),
                    message=full_message,
                )
                st.session_state["message_sent"] = True
                st.rerun()

# ===========================================================================
# EMBEDDED MAP PLACEHOLDER
# ===========================================================================
st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

map_card_html = (
    '<div class="contact-card" style="text-align:center; padding:3rem;">'
    '<div style="font-size:3rem; margin-bottom:1rem;">🗺️</div>'
    '<div class="info-card-title">Find Us on the Map</div>'
    '<p style="color:#9a9a9a;">'
    '124 Main Street, Brooklyn, NY 11201<br>'
    '<em style="font-size:0.85rem;">(Nearest subway: Jay St–MetroTech — A, C, F trains)</em>'
    '</p>'
    '<p style="color:#9a9a9a; font-size:0.85rem; margin-top:1rem;">'
    '💡 In production: replace this card with an embedded Google Maps iframe using your API key.'
    '</p>'
    '</div>'
)
st.markdown(map_card_html, unsafe_allow_html=True)
