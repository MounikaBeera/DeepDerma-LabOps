
import streamlit as st


def render_brand_header():
    """Render the brand and horizontal page navigation."""
    current_page = st.get_option("browser.serverAddress")

    st.markdown(
        """
        <div class="brand-row">
            <div class="brand-lockup">
                <div class="brand-mark">✳</div>
                <div class="brand-copy">
                    <div class="brand-name">
                        DeepDerma <span>LabOps</span>
                    </div>
                    <div class="brand-sub">
                        SKIN IMAGE INSIGHTS · AI RESEARCH PROTOTYPE
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_cards():
    """Render the three introduction cards."""
    st.markdown('<div class="section-kicker">Inside the lab</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Three perspectives, one comparison.</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Each model uses its own training-compatible image preprocessing. '
        'Compare their top class outputs and see where predictions agree or differ.</div>',
        unsafe_allow_html=True,
    )

    feature_cols = st.columns(3, gap="medium")
    feature_data = [
        ("⌁", "Compare models", "Run DenseNet201, ResNet101 and EfficientNetB0 on the same uploaded image."),
        ("◉", "Explore class scores", "Review each model’s outputs across the four classes included in training."),
        ("♡", "Keep context in view", "Read concise class-reference notes and important limitations alongside results."),
    ]
    for col, (icon, title, description) in zip(feature_cols, feature_data):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-copy">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)


def render_safety_notice():
    """Render the medical safety notice."""
    st.markdown("---")
    st.markdown(
        """
        <div class="safety-box">
            <strong>Important health notice</strong><br>
            DeepDerma-LabOps is an educational research prototype, not a medical device.
            Do not use these outputs to diagnose a condition or
            select treatment. Consult a qualified healthcare professional about
            concerning, changing or persistent skin lesions.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="footer">DeepDerma-LabOps · Built for learning, experimentation and model comparison.</div>',
        unsafe_allow_html=True,
    )



def render_hero():
    """Render the DeepDerma landing-page hero."""
    hero_left, hero_right = st.columns([1.25, 0.85], gap="large")

    with hero_left:
        st.markdown(
            """
            <div class="hero">
                <div class="eyebrow">✦ Three models. One workspace.</div>
                <h1>A closer look at skin, <span>powered by AI.</span></h1>
                <div class="hero-copy">
                    Explore an educational skin-image classification workflow
                    that compares three fine-tuned deep-learning models side by side.
                    Thoughtfully designed for experimentation, transparency and learning.
                </div>
                <div class="hero-foot">
                    DENSENET201 &nbsp;·&nbsp; RESNET101 &nbsp;·&nbsp; EFFICIENTNETB0
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with hero_right:
        st.markdown(
            """
            <div class="hero-art">
                <div class="orb">
                    <div class="orb-inner">✳</div>
                </div>
                <div class="floating-tag tag-top">
                    <strong>3 AI models</strong>
                    Side-by-side comparison
                </div>
                <div class="floating-tag tag-bottom">
                    <strong>Research workspace</strong>
                    Built for learning
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
