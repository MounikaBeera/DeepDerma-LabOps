
from pathlib import Path
import sys

import streamlit as st

APP_DIR = Path(__file__).resolve().parent

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from components import render_brand_header


st.set_page_config(
    page_title="DeepDerma | AI Skin Image Lab",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CSS_PATH = APP_DIR / "static" / "style.css"

if CSS_PATH.exists():
    with open(CSS_PATH, "r", encoding="utf-8") as css_file:
        st.markdown(
            f"<style>{css_file.read()}</style>",
            unsafe_allow_html=True,
        )

# Register the app's pages centrally.
home_page = st.Page(
    "pages/01_Home.py",
    title="Home",
    default=True,
)

analysis_page = st.Page(
    "pages/02_Image_Analysis.py",
    title="Image Analysis",
)

# Hide Streamlit's automatic page navigation.
current_page = st.navigation(
    [home_page, analysis_page],
    position="hidden",
)

# Custom website-style header.
header_brand, header_nav = st.columns(
    [2.2, 1],
    vertical_alignment="center",
)

with header_brand:
    render_brand_header()

with header_nav:
    nav_home, nav_analysis = st.columns(2, gap="small")

    with nav_home:
        st.page_link(
            home_page,
            label="Home",
            use_container_width=True,
        )

    with nav_analysis:
        st.page_link(
            analysis_page,
            label="Image Analysis",
            use_container_width=True,
        )

# Render the selected page below the shared header.
current_page.run()
