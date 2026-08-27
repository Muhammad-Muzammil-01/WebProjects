# =============================================================================
# data.py — Static data for the Barber Shop app
# =============================================================================
# This file holds all the "hardcoded" data that doesn't need a database:
#   - The list of services offered (name, price, duration)
#   - The list of barbers on the team (name, specialty, image)
#
# Why keep this separate from database.py?
#   Services and barbers rarely change, so reading from a Python list is faster
#   than a DB round-trip. It also makes it easy to update for demos/interviews.
#   If the shop grew, you'd migrate these into DB tables and add CRUD pages.
# =============================================================================

# -----------------------------------------------------------------------------
# SERVICES — each entry is a dictionary with four keys:
#   "name"     : display name of the service
#   "price"    : price in USD (string with $ for display, float for math)
#   "duration" : how long the appointment takes (string for display)
#   "description": short text shown on the Services page card
# -----------------------------------------------------------------------------
SERVICES = [
    {
        "name": "Classic Haircut",            # most popular service
        "price": 25.00,                       # price as a float for easy comparison
        "duration": "30 min",                 # estimated session length
        "description": "Precision cut tailored to your style — scissor or clipper.",
    },
    {
        "name": "Beard Trim",                 # beard grooming service
        "price": 15.00,
        "duration": "20 min",
        "description": "Shape, line-up, and trim for a clean, defined beard.",
    },
    {
        "name": "Hot Towel Shave",            # traditional wet-shave experience
        "price": 30.00,
        "duration": "40 min",
        "description": "Old-school straight-razor shave with a hot towel finish.",
    },
    {
        "name": "Haircut + Beard Combo",      # bundled discount service
        "price": 35.00,
        "duration": "50 min",
        "description": "Full cut and beard groom together at a bundled rate.",
    },
    {
        "name": "Kids Haircut (Under 12)",    # separate pricing for children
        "price": 18.00,
        "duration": "25 min",
        "description": "Gentle, fuss-free cut for the little ones.",
    },
    {
        "name": "Hair Wash & Style",          # add-on / standalone styling
        "price": 20.00,
        "duration": "30 min",
        "description": "Shampoo, condition, blow-dry, and styled to perfection.",
    },
]

# -----------------------------------------------------------------------------
# BARBERS — each entry is a dictionary with four keys:
#   "name"      : barber's display name
#   "specialty" : their main skill/style focus
#   "bio"       : one-sentence background
#   "image_url" : URL to a royalty-free placeholder portrait
#                 (using DiceBear Avatars — SVG, no sign-up required)
# -----------------------------------------------------------------------------
BARBERS = [
    {
        "name": "Marcus Reeves",
        "specialty": "Fades & Tapers",        # specialty shown on team card
        "bio": "10 years of barbering experience. Fade king of the shop.",
        # DiceBear generates a unique illustrated avatar from the seed string
        "image_url": "https://api.dicebear.com/7.x/personas/svg?seed=Marcus",
    },
    {
        "name": "Jordan Lee",
        "specialty": "Classic Cuts & Shaves",
        "bio": "Old-school technique meets modern style. Loves a hot towel shave.",
        "image_url": "https://api.dicebear.com/7.x/personas/svg?seed=Jordan",
    },
    {
        "name": "Dante Rivera",
        "specialty": "Beard Sculpting",
        "bio": "Certified beard artist. No beard too complex to shape.",
        "image_url": "https://api.dicebear.com/7.x/personas/svg?seed=Dante",
    },
    {
        "name": "Alex Kim",
        "specialty": "Creative & Color Styles",
        "bio": "Pushes the boundary of traditional barbering with bold styles.",
        "image_url": "https://api.dicebear.com/7.x/personas/svg?seed=Alex",
    },
]

# -----------------------------------------------------------------------------
# SHOP INFO — static shop details used on Home and Contact pages
# -----------------------------------------------------------------------------
SHOP_INFO = {
    "name": "The Sharp Edge Barber Shop",      # shop display name
    "tagline": "Look Sharp. Feel Sharp.",      # hero tagline
    "address": "124 Main Street, Brooklyn, NY 11201",
    "phone": "(718) 555-0199",
    "email": "info@thesharpedge.com",
    # Opening hours as a list of tuples: (day label, hours string)
    "hours": [
        ("Monday – Thursday", "9:00 AM – 7:00 PM"),
        ("Friday",            "9:00 AM – 1:00 PM  |  3:00 PM – 7:00 PM (Break 1–3 PM)"),
        ("Saturday",          "8:00 AM – 6:00 PM"),
        ("Sunday",            "10:00 AM – 4:00 PM"),
    ],
}

# -----------------------------------------------------------------------------
# AVAILABLE TIME SLOTS — the half-hour slots a barber can be booked into.
# Stored as strings in "HH:MM" 24-hour format so they sort correctly and
# match what's stored in SQLite (TEXT column).
# The booking page converts these to 12-hour display strings for the UI.
# -----------------------------------------------------------------------------
TIME_SLOTS = [
    "09:00", "09:30",
    "10:00", "10:30",
    "11:00", "11:30",
    "12:00", "12:30",
    "13:00", "13:30",
    "14:00", "14:30",
    "15:00", "15:30",
    "16:00", "16:30",
    "17:00", "17:30",
    "18:00", "18:30",
]

# -----------------------------------------------------------------------------
# ADMIN PASSWORD — kept here for simplicity in a junior/demo project.
# In a real production app you would store this as an environment variable or
# a Streamlit secret (st.secrets["admin_password"]) and NEVER commit it to Git.
# For Streamlit Community Cloud, you'd add it under "Secrets" in the dashboard.
# -----------------------------------------------------------------------------
ADMIN_PASSWORD = "sharpedge2024"   # change this before deploying!
