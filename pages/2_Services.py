# =============================================================================
# pages/2_Services.py — Services Page
# =============================================================================
# Renders the full menu of services offered by the barber shop.
# Each service is a styled "card" generated dynamically from the SERVICES list
# in data.py — NOT hardcoded HTML. This is important: you can add a new service
# by adding one dict to data.py, and it automatically appears here.
#
# Demonstrates:
#   - Iterating over a Python list to generate dynamic HTML
#   - Separating data (data.py) from presentation (this file)
#   - Custom CSS card components
# =============================================================================

import streamlit as st
import os
import sys

# Add project root to path so we can import from data.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import SERVICES, SHOP_INFO   # import the services list and shop info

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Services | The Sharp Edge", page_icon="💈", layout="wide")

# ── CSS injection ─────────────────────────────────────────────────────────────
def load_css():
    """Loads the global CSS stylesheet."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# ===========================================================================
# PAGE HEADER
# ===========================================================================

st.markdown("""
    <h1>💈 Our Services</h1>
    <p style='color:#9a9a9a; font-size:1.05rem; margin-bottom:2rem;'>
        From classic cuts to full grooming packages — all services performed by
        our master barbers with professional-grade products.
    </p>
    <hr class="gold-divider">
""", unsafe_allow_html=True)


# ===========================================================================
# SERVICE CARDS — dynamically generated from the SERVICES list
# ===========================================================================
# We loop over SERVICES and render each one as an HTML card.
# The HTML string is built using an f-string, then passed to st.markdown().
# This means if you add a 7th service to data.py, it appears here automatically
# without touching this file at all.
# ===========================================================================

st.markdown("<h2>Menu & Pricing</h2>", unsafe_allow_html=True)

# Loop through every service in the list
# enumerate() gives us both the index (i) and the service dict in each iteration
for i, service in enumerate(SERVICES):

    # Format the price as a dollar string with 2 decimal places
    # e.g. 25.0 → "$25.00"
    price_display = f"${service['price']:.2f}"

    # Build the service card HTML using the service dict's values
    card_html = f"""
        <div class="service-card">
            <!-- Left side: service name and description -->
            <div style="flex:1;">
                <div class="service-name">✂️ {service['name']}</div>
                <div class="service-desc">{service['description']}</div>
            </div>

            <!-- Right side: price and duration -->
            <div class="service-meta">
                <div class="service-price">{price_display}</div>
                <span class="service-duration">⏱ {service['duration']}</span>
            </div>
        </div>
    """
    # Each card is its own markdown block — Streamlit renders them sequentially
    st.markdown(card_html, unsafe_allow_html=True)


# ===========================================================================
# SUMMARY STATS BAR
# ===========================================================================
# Quick metrics below the cards — calculated from the SERVICES data in Python.
# This shows that the data isn't just for display; we can compute things from it.
# ===========================================================================

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

# Calculate summary statistics from the SERVICES list
total_services  = len(SERVICES)                                      # count of all services
min_price       = min(s["price"] for s in SERVICES)                  # cheapest service
max_price       = max(s["price"] for s in SERVICES)                  # most expensive service
avg_price       = sum(s["price"] for s in SERVICES) / total_services # average price

# Display the stats in three metric columns using Streamlit's st.metric widget
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Total Services", total_services)   # shows the number in a bold box

with m2:
    st.metric("Starting From", f"${min_price:.2f}")   # cheapest option

with m3:
    st.metric("Premium Up To", f"${max_price:.2f}")   # most expensive

with m4:
    st.metric("Average Price", f"${avg_price:.2f}")   # average across all


# ===========================================================================
# PROMOTIONS / NOTES SECTION
# ===========================================================================

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

# Two info cards in columns: promotions on the left, policies on the right
promo_col, policy_col = st.columns(2)

with promo_col:
    st.markdown("""
        <div class="info-card">
            <div class="info-card-title">🎉 Current Promotions</div>
            <ul style="color:#f5f5f5; padding-left:1.2rem; line-height:2;">
                <li>First-time customers — 10% off any service</li>
                <li>Refer a friend — get a free beard trim</li>
                <li>Loyalty Card — 10th visit is free</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with policy_col:
    st.markdown("""
        <div class="info-card">
            <div class="info-card-title">📋 Booking Policy</div>
            <ul style="color:#f5f5f5; padding-left:1.2rem; line-height:2;">
                <li>Please arrive 5 minutes before your appointment</li>
                <li>Late arrivals may need to be rescheduled</li>
                <li>Cancellations: 24-hour notice appreciated</li>
                <li>Walk-ins welcome, subject to availability</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)


# ===========================================================================
# BOOK NOW CTA AT BOTTOM
# ===========================================================================

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

# Center-aligned CTA using a single column trick
_, center_col, _ = st.columns([2, 3, 2])   # side columns are spacers

with center_col:
    st.markdown("""
        <div style="text-align:center; padding:1.5rem;">
            <h3 style="color:#f5f5f5 !important; margin-bottom:0.5rem;">
                Ready to book?
            </h3>
            <p style="color:#9a9a9a; margin-bottom:1.5rem;">
                Choose your service, pick your barber, and lock in your time slot.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Native Streamlit button — navigates to the booking page
    if st.button("📅 Book an Appointment", use_container_width=True):
        st.switch_page("pages/4_Book_Appointment.py")
