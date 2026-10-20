
from pathlib import Path
import sys
import time
from database import (create_experiment,get_model_id,save_prediction,record_audit_event,update_experiment_status,)
# Make the parent app directory available for imports.
APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from collections import Counter

import streamlit as st
import numpy as np
from PIL import Image, UnidentifiedImageError

from model_service import predict_with_model
from condition_data import CONDITION_INFO


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = APP_DIR.parent
MODEL_DIR = PROJECT_ROOT / "models"
CSS_PATH = APP_DIR / "static" / "style.css"

with open(CSS_PATH, "r", encoding="utf-8") as css_file:
    st.markdown(
        f"<style>{css_file.read()}</style>",
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# 2. MODEL CONFIGURATION
# --------------------------------------------------
CLASS_LABELS = [
    "Actinic keratosis",
    "Atopic Dermatitis",
    "Benign keratosis",
    "Dermatofibroma",
]

MODEL_CONFIG = {
    "DenseNet201": {
        "filename": "densenet201_finetuned_best.keras",
        "preprocessing": "densenet",
        "accuracy": "88.89%",
        "short": "Dense feature connections",
    },
    "ResNet101": {
        "filename": "resnet101_finetuned_best.keras",
        "preprocessing": "resnet",
        "accuracy": "90.12%",
        "short": "Residual learning",
    },
    "EfficientNetB0": {
        "filename": "efficientnetb0_finetuned_best.keras",
        "preprocessing": "efficientnet",
        "accuracy": "88.89%",
        "short": "Efficient architecture",
    },
}


# --------------------------------------------------
# 3. PAGE HEADER
# --------------------------------------------------
st.markdown(
    '<div class="section-kicker">02 / IMAGE LAB</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-title">Skin image analysis</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-copy">Upload a clear JPG or PNG image to '
    'compare DenseNet201, ResNet101, and EfficientNetB0. This educational '
    'prototype does not provide a medical diagnosis.</div>',
    unsafe_allow_html=True,
)


# --------------------------------------------------
# 4. UPLOAD AND IMAGE PREVIEW
# --------------------------------------------------
upload_col, preview_col = st.columns([0.92, 1.08], gap="large")

with upload_col:
    st.markdown(
        '<div class="upload-heading"><span>01 /</span> Upload an image</div>',
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        "Choose a JPG or PNG file",
        type=["jpg", "jpeg", "png"],
        help="Use a readable image file. Avoid uploading identifying information.",
        key="skin_image_uploader",
    )
    st.markdown(
        '<p class="small-muted">Tip: use a well-lit, focused image. '
        'Image quality and dataset differences can affect model outputs.</p>',
        unsafe_allow_html=True,
    )

image = None

if uploaded_file is not None:
    try:
        uploaded_file.seek(0)
        with Image.open(uploaded_file) as check_image:
            check_image.verify()

        uploaded_file.seek(0)
        with Image.open(uploaded_file) as opened_image:
            image = opened_image.convert("RGB")

        if image.width < 32 or image.height < 32:
            st.error("Please upload an image at least 32 × 32 pixels.")
            image = None
        elif image.width * image.height > 25_000_000:
            st.error("This image exceeds the 25-megapixel limit.")
            image = None

    except (UnidentifiedImageError, OSError, ValueError):
        st.error("We couldn't read that image. Please try a valid JPG or PNG.")
        image = None

with preview_col:
    st.markdown(
        '<div class="upload-heading"><span>02 /</span> Image preview</div>',
        unsafe_allow_html=True,
    )

    if image is not None:
        st.image(
            image,
            caption=f"Preview · {image.width} × {image.height} px",
            use_container_width=True,
        )
        st.markdown(
            f'<p class="small-muted">File: {uploaded_file.name}</p>',
            unsafe_allow_html=True,
        )
    else:
        st.info("Your uploaded image preview will appear here.")


# --------------------------------------------------
# 5. ANALYSIS CONTROLS
# --------------------------------------------------
analyze_col, reset_col = st.columns(2)

with analyze_col:
    analyze_clicked = st.button(
        "Run model comparison  ↗",
        type="primary",
        use_container_width=True,
        disabled=image is None,
    )

with reset_col:
    if st.button("Clear current results", use_container_width=True):
        st.session_state.pop("last_results", None)
        st.session_state.pop("last_errors", None)
        st.session_state.pop("last_filename", None)
        st.rerun()


# --------------------------------------------------
# 6. RUN THE THREE MODELS
# --------------------------------------------------
if analyze_clicked and image is not None:
    results = {}
    errors = {}

    experiment_id = None

    try:
        experiment_id = create_experiment(
            experiment_name="Three-model image analysis",
            notes="Image analysis initiated from the DeepDerma Streamlit app.",
        )
        st.caption(f"Experiment ID: {experiment_id}")
    except Exception as experiment_error:
        st.warning(
            "Could not create a database experiment. "
            "Predictions will still run, but cannot be linked "
            f"to an experiment. Error: {experiment_error}"
        )

    progress = st.progress(0.0, text="Preparing analysis…")
    status = st.empty()

    for index, (model_name, config) in enumerate(MODEL_CONFIG.items()):
        status.write(f"Running **{model_name}**…")

        try:
            started_at = time.perf_counter()

            result = predict_with_model(
                image,
                model_name,
                config,
                model_dir=MODEL_DIR,
                class_labels=CLASS_LABELS,
            )

            duration_ms = round(
                (time.perf_counter() - started_at) * 1000
            )

            # Keep the model result available even if SQL Server is unavailable.
            results[model_name] = result

            try:
                model_id = get_model_id(model_name)

                if model_id is None:
                    raise ValueError(
                        f"{model_name} is not registered as an active model."
                    )

                scores = {
                    label: float(result["scores"][index])
                    for index, label in enumerate(CLASS_LABELS)
                }

                prediction_id = save_prediction(
                    model_id=model_id,
                    predicted_class=result["predicted_class"],
                    confidence=float(result["confidence"]),
                    scores=scores,
                    duration_ms=duration_ms,
                    experiment_id=experiment_id,
                )

                st.toast(
                    f"{model_name}: prediction saved to database "
                    f"(ID {prediction_id})"
                )

            except Exception as db_error:
                st.error(
                    f"Database save failed for {model_name}: "
                    f"{type(db_error).__name__}: {db_error}"
                )

        except Exception as error:
            errors[model_name] = f"{type(error).__name__}: {error}"

        progress.progress(
            (index + 1) / len(MODEL_CONFIG),
            text=f"{index + 1} of {len(MODEL_CONFIG)} models checked",
        )

    if experiment_id is not None:
        try:
            final_status = (
                "Completed"
                if results and not errors
                else "Failed"
            )

            update_experiment_status(
                experiment_id,
                final_status,
            )

            st.caption(
                f"Experiment {experiment_id} status: {final_status}"
            )

        except Exception as status_error:
            st.warning(
                "Predictions were processed, but the experiment "
                f"status could not be updated: {status_error}"
            )

    status.empty()
    progress.empty()

    st.session_state["last_results"] = results
    st.session_state["last_errors"] = errors
    st.session_state["last_filename"] = uploaded_file.name


# --------------------------------------------------
# 7. DISPLAY ERRORS
# --------------------------------------------------
results = st.session_state.get("last_results", {})
errors = st.session_state.get("last_errors", {})

if errors:
    st.warning(
        "One or more models could not complete the comparison. "
        "Check that the model files exist in the project's models folder."
    )
    with st.expander("Technical details"):
        for model_name, message in errors.items():
            st.write(f"**{model_name}:** `{message}`")


# --------------------------------------------------
# 8. RESULTS AND MODEL INSIGHTS
# --------------------------------------------------
if results:
    predicted_classes = [
        result["predicted_class"]
        for result in results.values()
        if "predicted_class" in result
    ]

    if predicted_classes:
        class_counts = Counter(predicted_classes)
        top_class, agreement_count = class_counts.most_common(1)[0]

        st.markdown("---")
        st.markdown(
            f"""
            <section class="dd-prediction-summary">
                <p class="dd-summary-eyebrow">YOUR IMAGE ANALYSIS</p>
                <h3>Top predicted class</h3>
                <h2>{top_class}</h2>
                <p>{agreement_count} of {len(predicted_classes)}
                completed models predicted this class.</p>
                <div class="dd-summary-note">
                    <strong>Important limitation</strong>
                    <p>This is an AI-generated classification, not a
                    confirmed diagnosis. Consult a qualified dermatologist
                    for assessment.</p>
                </div>
            </section>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-title">Results and model insights</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="section-copy">Results for '
        f'<strong>{st.session_state.get("last_filename", "uploaded image")}</strong>. '
        'Scores are raw model outputs, not clinically calibrated probabilities.</div>',
        unsafe_allow_html=True,
    )

    result_columns = st.columns(len(results), gap="medium")

    for column, (model_name, result) in zip(result_columns, results.items()):
        with column:
            st.markdown(
                f"""
                <div class="model-card">
                    <div class="model-label">Model output</div>
                    <div class="model-name">{model_name}</div>
                    <div class="prediction-name">{result["predicted_class"]}</div>
                    <div class="score-pill">Top score · {result["confidence"]:.2f}%</div>
                    <p class="small-muted" style="margin-top:.7rem;">
                        Validation accuracy: {MODEL_CONFIG[model_name]["accuracy"]}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("#### Prediction agreement")

    if len(results) == len(MODEL_CONFIG) and len(set(predicted_classes)) == 1:
        st.success(
            "All three models returned the same class. Agreement alone "
            "does not confirm a diagnosis."
        )
    elif len(set(predicted_classes)) > 1:
        st.warning(
            "The models returned different classes. Disagreement highlights "
            "uncertainty; it does not establish which output is correct."
        )
    else:
        st.info(
            f"{len(results)} of {len(MODEL_CONFIG)} models completed. "
            "Full agreement cannot be assessed."
        )

    st.markdown("#### Explore all class scores")

    for model_name, result in results.items():
        with st.expander(f"{model_name} · detailed class scores"):
            for class_index, label in enumerate(CLASS_LABELS):
                score = float(result["scores"][class_index] * 100)
                st.write(f"**{label}** — {score:.2f}%")
                st.progress(min(max(score / 100.0, 0.0), 1.0))

    st.markdown("#### Predicted-class reference")

    for model_name, result in results.items():
        predicted_class = result["predicted_class"]

        with st.expander(f"{model_name}: {predicted_class}"):
            st.write(CONDITION_INFO[predicted_class]["description"])
            st.markdown("**Associated factors**")
            st.write(CONDITION_INFO[predicted_class]["cause"])

else:
    st.markdown("---")
    st.markdown(
        '<div class="soft-panel"><strong>Your results will appear here.</strong>'
        '<p>Upload an image and run the comparison to explore the three '
        'model outputs, their agreement, and their class scores.</p></div>',
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# 9. SAFETY NOTICE
# --------------------------------------------------
st.markdown("---")
st.warning(
    "DeepDerma-LabOps is an educational research prototype, not a medical "
    "device. Model predictions and validation metrics must not be used to "
    "diagnose, rule out, or treat a skin condition."
)
