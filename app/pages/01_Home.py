
from pathlib import Path
import sys

import streamlit as st

APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from components import (
    render_feature_cards,
    render_safety_notice,
    render_hero,
)
from condition_data import CONDITION_INFO


CSS_PATH = APP_DIR / "static" / "style.css"


def load_css():
    if CSS_PATH.exists():
        with open(CSS_PATH, "r", encoding="utf-8") as css_file:
            st.markdown(
                f"<style>{css_file.read()}</style>",
                unsafe_allow_html=True,
            )


def render_condition_guide():
    st.markdown("---")
    st.markdown(
        '<div class="section-kicker">01 / Learn</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-title">Skin condition guide</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-copy">'
        "Explore the four skin-condition classes represented in this "
        "project's training dataset. These notes are educational, "
        "not a way to diagnose a skin condition."
        "</div>",
        unsafe_allow_html=True,
    )

    for condition_name, info in CONDITION_INFO.items():
        with st.expander(condition_name, expanded=False):
            st.write(info["description"])

            st.markdown("**Common symptoms or appearances**")
            for symptom in info.get("symptoms", []):
                st.markdown(f"- {symptom}")

            st.markdown("**Associated factors**")
            st.write(info["cause"])

            for factor in info.get("factors", []):
                st.markdown(f"- {factor}")

            references = info.get("references", [])
            if references:
                st.markdown("**Further reading**")
                for reference in references:
                    st.markdown(
                        f"- [{reference['name']}]({reference['url']})"
                    )

    st.caption(
        "A model class is not a confirmed diagnosis. In particular, "
        "'Benign keratosis' is a broad label and does not identify "
        "a specific lesion subtype. Seek professional assessment "
        "for a new, changing, bleeding, or concerning lesion."
    )


load_css()


render_hero()

render_feature_cards()
render_condition_guide()


st.markdown("---")

cta_col, button_col = st.columns([2.2, 1], gap="large")

with cta_col:
    st.markdown(
        '<div class="section-kicker">YOUR NEXT STEP</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-title">A closer look starts here.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-copy">'
        "Explore an image with AI-generated insights, review the "
        "results in a clear and simple format, and learn more about "
        "the skin-condition categories represented in this project."
        "</div>",
        unsafe_allow_html=True,
    )

with button_col:
    st.write("")
    st.write("")
    st.page_link(
        "pages/02_Image_Analysis.py",
        label="Explore your image ↗",
        icon=":material/arrow_forward:",
        use_container_width=True,
    )

st.caption(
    "For educational purposes only. AI-generated results cannot "
    "confirm or rule out a skin condition."
)

render_safety_notice()
