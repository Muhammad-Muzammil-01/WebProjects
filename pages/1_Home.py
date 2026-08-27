# =============================================================================
# pages/1_Home.py — Home Page
# =============================================================================
# This is the landing/welcome page. It contains:
#   1. A hero section (shop name, tagline, Book Now button)
#   2. Shop hours displayed in a styled table
#   3. Location and contact info in an info card
#
# All content is rendered with custom HTML/CSS injected via st.markdown().
# The static data (shop name, hours, etc.) is imported from data.py so there's
# no magic strings buried here — everything comes from one source of truth.
# =============================================================================

import streamlit as st          # Streamlit UI framework
import os                       # for file path construction
import sys                      # for modifying Python's module search path

# ---------------------------------------------------------------------------
# PATH SETUP
# ---------------------------------------------------------------------------
# Streamlit runs each page file in its own context. To import our custom
# modules (data.py, database.py) which live in the PARENT folder, we add
# that parent directory to sys.path so Python can find them.
# ---------------------------------------------------------------------------
# os.path.abspath(__file__) → absolute path of THIS file (1_Home.py)
# os.path.dirname(...)      → folder containing it (the 'pages' folder)
# os.path.dirname(...again) → parent of that (the project root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import SHOP_INFO   # shop name, tagline, hours, address

# ---------------------------------------------------------------------------
# PAGE TITLE (shown in browser tab for this page)
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Home | The Sharp Edge", page_icon="🏠", layout="wide")

# ---------------------------------------------------------------------------
# INJECT CSS (same stylesheet loaded in app.py, but pages need it too)
# ---------------------------------------------------------------------------
def load_css():
    """Loads and injects the global CSS stylesheet into the page."""
    # Build path: go up one level from /pages to the project root
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()   # call immediately when the page loads


# ===========================================================================
# SECTION 1: HERO BANNER
# ===========================================================================
# The hero uses raw HTML/CSS injected via st.markdown.
# We pull the shop name and tagline from SHOP_INFO so they're consistent
# across every page that uses them.
# The "Book Now" button links to page 4 using Streamlit's ?page= URL param.
# ===========================================================================

# f-string lets us insert Python variables into the HTML template
hero_html = f"""
<div class="hero-section">
    <!-- Shop name as the main heading -->
    <h1 class="hero-title">{SHOP_INFO['name']}</h1>

    <!-- Tagline below the title -->
    <p class="hero-tagline">"{SHOP_INFO['tagline']}"</p>

    <!-- Decorative scissors emoji as a visual separator -->
    <div style="font-size:2rem; margin: 1rem 0; color:#c9a84c;">✂ ✂ ✂</div>

    <!-- Subheading / value proposition -->
    <p style="color:#f5f5f5; font-size:1.1rem; max-width:600px; margin:0 auto 1.5rem;">
        Brooklyn's finest cuts, fades, and grooming — where tradition meets style.
        Walk in or book your appointment below.
    </p>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

_, hero_btn_col, _ = st.columns([2, 2, 2])
with hero_btn_col:
    if st.button("📅 Book Your Appointment", key="home_hero_btn", use_container_width=True, type="primary"):
        st.switch_page("pages/4_Book_Appointment.py")

st.markdown("<br>", unsafe_allow_html=True)


# ===========================================================================
# SECTION 2: INFO COLUMNS (Hours + Location side by side)
# ===========================================================================
# st.columns(2) creates a two-column grid layout.
# col1 gets the hours table; col2 gets the address/contact info.
# ===========================================================================

col1, col2 = st.columns(2)    # unpack into two column objects

# ---- LEFT COLUMN: Opening Hours ----------------------------------------

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


# ---- RIGHT COLUMN: Location & Contact ----------------------------------

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


# ===========================================================================
# SECTION 3: WHY CHOOSE US — Three value-proposition columns
# ===========================================================================

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)  # decorative divider

# Section heading
st.markdown("<h2 style='text-align:center;'>Why Choose The Sharp Edge?</h2>",
            unsafe_allow_html=True)

# Three equal-width columns for the feature highlights
feat1, feat2, feat3 = st.columns(3)

# Each feature uses the same info-card HTML template but with different icons/text
features = [
    ("✂️", "Master Barbers",
     "Our barbers each bring 7–15 years of professional experience. Precision in every cut."),
    ("⭐", "Premium Products",
     "We only use top-shelf grooming products — Proraso, American Crew, and more."),
    ("📅", "Easy Booking",
     "Book online in under 60 seconds. No phone tag. No waiting. Just show up looking great."),
]

# Loop through features and render each in its column
for col, (icon, title, desc) in zip([feat1, feat2, feat3], features):
    with col:
        st.markdown(f"""
            <div class="info-card" style="text-align:center;">
                <div style="font-size:2.5rem; margin-bottom:0.8rem;">{icon}</div>
                <div class="info-card-title">{title}</div>
                <p style="color:#9a9a9a; font-size:0.9rem; margin:0;">{desc}</p>
            </div>
        """, unsafe_allow_html=True)


# ===========================================================================
# SECTION 4: QUICK CALL-TO-ACTION STRIP at the bottom
# ===========================================================================

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

# Bottom CTA row — two columns: left = text, right = button
cta_left, cta_right = st.columns([3, 1])

with cta_left:
    st.markdown("""
        <h3 style="margin:0; color:#f5f5f5 !important;">
            Ready for your next great look?
        </h3>
        <p style="color:#9a9a9a; margin:0.4rem 0 0;">
            Book your appointment online — available 24/7.
        </p>
    """, unsafe_allow_html=True)

with cta_right:
    # Streamlit native button that shows a navigation hint
    # (Full redirect requires session_state + st.switch_page in newer Streamlit)
    if st.button("📅 Book Now", use_container_width=True):
        # st.switch_page navigates to a page in the /pages folder
        # The string must match the filename (without leading number prefix in newer versions)
        st.switch_page("pages/4_Book_Appointment.py")
