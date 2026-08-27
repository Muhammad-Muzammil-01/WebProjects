# =============================================================================
# app.py — Main entry point for The Sharp Edge Barber Shop Streamlit app
# =============================================================================
import streamlit as st
import os
import sys

# Add root folder to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import init_db
from data import SHOP_INFO

# ---------------------------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="The Sharp Edge Barber Shop",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com",
        "About": "The Sharp Edge Barber Shop — Portfolio project built with Streamlit & SQLite.",
    },
)

# ---------------------------------------------------------------------------
# LOAD AND INJECT CUSTOM CSS
# ---------------------------------------------------------------------------
def load_css(css_file_path: str) -> None:
    """Reads a CSS file and injects it into the page."""
    if os.path.exists(css_file_path):
        with open(css_file_path, "r", encoding="utf-8") as css_file:
            css_content = css_file.read()
        st.markdown(f"<style>\n{css_content}\n</style>", unsafe_allow_html=True)


CSS_PATH = os.path.join(os.path.dirname(__file__), "style.css")
load_css(CSS_PATH)

# ---------------------------------------------------------------------------
# DATABASE INITIALISATION
# ---------------------------------------------------------------------------
if "db_initialised" not in st.session_state:
    init_db()
    st.session_state["db_initialised"] = True

# ---------------------------------------------------------------------------
# SIDEBAR BRANDING
# ---------------------------------------------------------------------------
with st.sidebar:
    sidebar_brand = (
        '<div style="text-align:center; padding: 1rem 0 0.5rem;">'
        '<div style="font-size:2rem;">✂️</div>'
        '<div style="font-family:\'Playfair Display\',serif; color:#c9a84c; font-size:1.1rem; font-weight:700; letter-spacing:0.05em; margin-top:0.3rem;">'
        'The Sharp Edge'
        '</div>'
        '<div style="color:#9a9a9a; font-size:0.75rem; margin-top:0.2rem;">'
        'Premium Barber Shop'
        '</div>'
        '</div>'
        '<hr style="border-color:#2e2e2e; margin:0.8rem 0;">'
    )
    st.markdown(sidebar_brand, unsafe_allow_html=True)

# ===========================================================================
# HOME PAGE CONTENT
# ===========================================================================

# ── HERO SECTION ──────────────────────────────────────────────────────────
hero_html = (
    '<div class="hero-section">'
    f'<h1 class="hero-title">{SHOP_INFO["name"]}</h1>'
    f'<p class="hero-tagline">"{SHOP_INFO["tagline"]}"</p>'
    '<div style="font-size:2rem; margin: 1rem 0; color:#c9a84c;">✂ ✂ ✂</div>'
    '<p style="color:#f5f5f5; font-size:1.1rem; max-width:600px; margin:0 auto 1.5rem;">'
    'Brooklyn\'s finest cuts, fades, and grooming — where tradition meets style. Walk in or book your appointment below.'
    '</p>'
    '</div>'
)
st.markdown(hero_html, unsafe_allow_html=True)

# ── DIRECT BOOK BUTTON UNDER HERO ─────────────────────────────────────────
_, hero_btn_col, _ = st.columns([2, 2, 2])
with hero_btn_col:
    if st.button("📅 Book Your Appointment", key="hero_book_btn", use_container_width=True, type="primary"):
        st.switch_page("pages/4_Book_Appointment.py")

st.markdown("<br>", unsafe_allow_html=True)

# ── INFO COLUMNS: Hours & Location ────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    hours_rows = "".join([
        f'<tr><td style="padding:0.4rem 1rem 0.4rem 0; color:#9a9a9a; font-size:0.92rem;">{day}</td>'
        f'<td style="padding:0.4rem 0; color:#f5f5f5; font-size:0.92rem; font-weight:600;">{hours}</td></tr>'
        for day, hours in SHOP_INFO["hours"]
    ])
    hours_card_html = (
        '<div class="info-card">'
        '<div class="info-card-title">🕐 Opening Hours</div>'
        '<table style="border-collapse:collapse; width:100%;">'
        f'<tbody>{hours_rows}</tbody>'
        '</table>'
        '</div>'
    )
    st.markdown(hours_card_html, unsafe_allow_html=True)

with col2:
    location_html = (
        '<div class="info-card">'
        '<div class="info-card-title">📍 Find Us</div>'
        '<div class="contact-item">'
        '<span class="contact-icon">🗺️</span>'
        f'<span>{SHOP_INFO["address"]}</span>'
        '</div>'
        '<div class="contact-item">'
        '<span class="contact-icon">📞</span>'
        f'<span>{SHOP_INFO["phone"]}</span>'
        '</div>'
        '<div class="contact-item">'
        '<span class="contact-icon">✉️</span>'
        f'<span>{SHOP_INFO["email"]}</span>'
        '</div>'
        '<hr style="border-color:#2e2e2e; margin:1rem 0;">'
        '<div class="contact-item">'
        '<span class="contact-icon">🅿️</span>'
        '<span style="color:#9a9a9a; font-size:0.9rem;">Street parking available. Nearest subway: Jay St–MetroTech (A/C/F)</span>'
        '</div>'
        '</div>'
    )
    st.markdown(location_html, unsafe_allow_html=True)

# ── VALUE PROPOSITIONS ───────────────────────────────────────────────────
st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>Why Choose The Sharp Edge?</h2>", unsafe_allow_html=True)

feat1, feat2, feat3 = st.columns(3)
features = [
    ("✂️", "Master Barbers", "Our barbers each bring 7–15 years of professional experience. Precision in every cut."),
    ("⭐", "Premium Products", "We only use top-shelf grooming products — Proraso, American Crew, and more."),
    ("📅", "Easy Booking", "Book online in under 60 seconds. No phone tag. No waiting. Just show up looking great."),
]

for col, (icon, title, desc) in zip([feat1, feat2, feat3], features):
    with col:
        card = (
            '<div class="info-card" style="text-align:center;">'
            f'<div style="font-size:2.5rem; margin-bottom:0.8rem;">{icon}</div>'
            f'<div class="info-card-title">{title}</div>'
            f'<p style="color:#9a9a9a; font-size:0.9rem; margin:0;">{desc}</p>'
            '</div>'
        )
        st.markdown(card, unsafe_allow_html=True)

# ── BOTTOM CTA ───────────────────────────────────────────────────────────
st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

cta_left, cta_right = st.columns([3, 1])
with cta_left:
    st.markdown(
        '<h3 style="margin:0; color:#f5f5f5 !important;">Ready for your next great look?</h3>'
        '<p style="color:#9a9a9a; margin:0.4rem 0 0;">Book your appointment online — available 24/7.</p>',
        unsafe_allow_html=True
    )

with cta_right:
    if st.button("📅 Book Now", key="bottom_book_btn", use_container_width=True):
        st.switch_page("pages/4_Book_Appointment.py")
