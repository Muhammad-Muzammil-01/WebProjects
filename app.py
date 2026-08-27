# =============================================================================
# app.py — Main entry point for The Sharp Edge Barber Shop Streamlit app
# =============================================================================
# This file does three things:
#   1. Configures the Streamlit page (title, icon, layout)
#   2. Loads and injects the global CSS stylesheet
#   3. Initialises the database once on first run
#   4. Renders the full Home page experience
#
# Navigation is handled automatically by Streamlit's multi-page app system:
# any .py file placed in the /pages folder becomes a sidebar page.
# =============================================================================

import streamlit as st      # the entire app UI framework
import os                   # for building file paths
import sys                  # for module imports

# Add root folder to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import database initialization and shop info
from database import init_db
from data import SHOP_INFO


# ---------------------------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="The Sharp Edge Barber Shop",   # shown in browser tab
    page_icon="✂️",                             # emoji as the favicon
    layout="wide",                              # use full browser width
    initial_sidebar_state="expanded",           # sidebar open by default
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
    st.markdown("""
        <div style='text-align:center; padding: 1rem 0 0.5rem;'>
            <div style='font-size:2rem;'>✂️</div>
            <div style='font-family:"Playfair Display",serif;
                        color:#c9a84c; font-size:1.1rem; font-weight:700;
                        letter-spacing:0.05em; margin-top:0.3rem;'>
                The Sharp Edge
            </div>
            <div style='color:#9a9a9a; font-size:0.75rem; margin-top:0.2rem;'>
                Premium Barber Shop
            </div>
        </div>
        <hr style='border-color:#2e2e2e; margin:0.8rem 0;'>
    """, unsafe_allow_html=True)


# ===========================================================================
# HOME PAGE CONTENT
# ===========================================================================

# ── HERO SECTION ──────────────────────────────────────────────────────────
hero_html = f"""
<div class="hero-section">
    <h1 class="hero-title">{SHOP_INFO['name']}</h1>
    <p class="hero-tagline">"{SHOP_INFO['tagline']}"</p>
    <div style="font-size:2rem; margin: 1rem 0; color:#c9a84c;">✂ ✂ ✂</div>
    <p style="color:#f5f5f5; font-size:1.1rem; max-width:600px; margin:0 auto 2rem;">
        Brooklyn's finest cuts, fades, and grooming — where tradition meets style.
        Walk in or book your appointment below.
    </p>
</div>
"""
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
    st.markdown("""
        <div class="info-card">
            <div class="info-card-title">🕐 Opening Hours</div>
    """, unsafe_allow_html=True)

    hours_rows = ""
    for day, hours in SHOP_INFO["hours"]:
        hours_rows += f"""
            <tr>
                <td style="padding:0.4rem 1rem 0.4rem 0; color:#9a9a9a; font-size:0.92rem;">{day}</td>
                <td style="padding:0.4rem 0; color:#f5f5f5; font-size:0.92rem; font-weight:600;">{hours}</td>
            </tr>
        """

    hours_table_html = f"""
        <table style="border-collapse:collapse; width:100%;">
            <tbody>
                {hours_rows}
            </tbody>
        </table>
        </div>
    """
    st.markdown(hours_table_html, unsafe_allow_html=True)


with col2:
    location_html = f"""
        <div class="info-card">
            <div class="info-card-title">📍 Find Us</div>
            <div class="contact-item">
                <span class="contact-icon">🗺️</span>
                <span>{SHOP_INFO['address']}</span>
            </div>
            <div class="contact-item">
                <span class="contact-icon">📞</span>
                <span>{SHOP_INFO['phone']}</span>
            </div>
            <div class="contact-item">
                <span class="contact-icon">✉️</span>
                <span>{SHOP_INFO['email']}</span>
            </div>
            <hr style="border-color:#2e2e2e; margin:1rem 0;">
            <div class="contact-item">
                <span class="contact-icon">🅿️</span>
                <span style="color:#9a9a9a; font-size:0.9rem;">
                    Street parking available. Nearest subway: Jay St–MetroTech (A/C/F)
                </span>
            </div>
        </div>
    """
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
        st.markdown(f"""
            <div class="info-card" style="text-align:center;">
                <div style="font-size:2.5rem; margin-bottom:0.8rem;">{icon}</div>
                <div class="info-card-title">{title}</div>
                <p style="color:#9a9a9a; font-size:0.9rem; margin:0;">{desc}</p>
            </div>
        """, unsafe_allow_html=True)


# ── BOTTOM CTA ───────────────────────────────────────────────────────────
st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

cta_left, cta_right = st.columns([3, 1])
with cta_left:
    st.markdown("""
        <h3 style="margin:0; color:#f5f5f5 !important;">Ready for your next great look?</h3>
        <p style="color:#9a9a9a; margin:0.4rem 0 0;">Book your appointment online — available 24/7.</p>
    """, unsafe_allow_html=True)

with cta_right:
    if st.button("📅 Book Now", key="bottom_book_btn", use_container_width=True):
        st.switch_page("pages/4_Book_Appointment.py")
