# =============================================================================
# app.py — Main entry point for The Sharp Edge Barber Shop Streamlit app
# =============================================================================
# This file does three things:
#   1. Configures the Streamlit page (title, icon, layout)
#   2. Loads and injects the global CSS stylesheet
#   3. Initialises the database once on first run
#
# Navigation is handled automatically by Streamlit's multi-page app system:
# any .py file placed in the /pages folder becomes a sidebar page.
# The order is controlled by the numeric prefix in the filename (1_, 2_, etc.)
#
# Run this app with:   streamlit run app.py
# =============================================================================

import streamlit as st      # the entire app UI framework
import os                   # for building file paths

# Import our own database initialisation function
# (database.py lives in the same folder as this file)
from database import init_db


# ---------------------------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------------------------
# st.set_page_config MUST be the first Streamlit call in app.py
# (Streamlit throws an error if anything else runs before it)
st.set_page_config(
    page_title="The Sharp Edge Barber Shop",   # shown in browser tab
    page_icon="✂️",                             # emoji as the favicon
    layout="wide",                              # use full browser width
    initial_sidebar_state="expanded",           # sidebar open by default
    menu_items={
        # These appear in the ⋮ hamburger menu top-right
        "Get Help": "https://github.com",
        "About": "The Sharp Edge Barber Shop — Portfolio project built with Streamlit & SQLite.",
    },
)


# ---------------------------------------------------------------------------
# LOAD AND INJECT CUSTOM CSS
# ---------------------------------------------------------------------------
# We read style.css from disk and wrap it in a <style> tag.
# st.markdown with unsafe_allow_html=True tells Streamlit to render raw HTML.
# The 'unsafe' label is a warning that YOU are responsible for what's inside —
# safe here because we're loading our own file, not user input.
def load_css(css_file_path: str) -> None:
    """
    Reads a CSS file from disk and injects it as a <style> block into the page.

    Parameters:
        css_file_path (str): Absolute or relative path to the .css file.

    Returns: None

    Why inject CSS this way?
        Streamlit doesn't have a native "load stylesheet" function.
        This is the community-standard workaround. The CSS applies globally
        to every page because app.py is executed before each page renders.
    """
    # Open the CSS file in read mode with UTF-8 encoding
    with open(css_file_path, "r", encoding="utf-8") as css_file:
        css_content = css_file.read()   # read the entire file as a string

    # Wrap the CSS in a <style> tag and inject it into the Streamlit page
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


# Build an absolute path to style.css so it works regardless of where the
# app is launched from.
# os.path.dirname(__file__) = directory containing app.py
# os.path.join combines it with the filename safely
CSS_PATH = os.path.join(os.path.dirname(__file__), "style.css")

# Only inject CSS if the file actually exists (prevents cryptic errors)
if os.path.exists(CSS_PATH):
    load_css(CSS_PATH)


# ---------------------------------------------------------------------------
# DATABASE INITIALISATION
# ---------------------------------------------------------------------------
# init_db() creates the tables if they don't already exist.
# Calling it here (in app.py) guarantees tables exist before ANY page runs.
# We use st.session_state to make sure we only call it once per session,
# not on every Streamlit rerun (which happens whenever the user interacts).

# st.session_state is a dict-like object that persists across reruns
# for the same browser session — like a "server-side session variable."
if "db_initialised" not in st.session_state:
    init_db()                           # create tables if needed
    st.session_state["db_initialised"] = True   # set the flag so we skip next time


# ---------------------------------------------------------------------------
# SIDEBAR BRANDING
# ---------------------------------------------------------------------------
# This renders in the sidebar on EVERY page because app.py runs on every page load.
# Streamlit's multi-page system re-runs app.py's sidebar code each time.

with st.sidebar:
    # Shop logo / name in the sidebar header
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


# ---------------------------------------------------------------------------
# HOME PAGE REDIRECT CONTENT
# ---------------------------------------------------------------------------
# When a user hits the root URL (just app.py), show a welcome message.
# The actual Home page is pages/1_Home.py, but this gives a nice landing.

st.markdown("""
    <div style='text-align:center; padding: 5rem 2rem;'>
        <div style='font-size:4rem;'>✂️</div>
        <h1 style='font-family:"Playfair Display",serif; color:#c9a84c;
                   font-size:2.5rem; margin:1rem 0 0.5rem;'>
            The Sharp Edge Barber Shop
        </h1>
        <p style='color:#9a9a9a; font-size:1.1rem; font-style:italic;'>
            Look Sharp. Feel Sharp.
        </p>
        <p style='color:#f5f5f5; margin-top:1.5rem;'>
            👈 Use the sidebar to navigate between pages.
        </p>
    </div>
""", unsafe_allow_html=True)
