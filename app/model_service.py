
from pathlib import Path

import numpy as np
import streamlit as st
import tensorflow as tf


# --------------------------------------------------
# MODEL LOADING
# --------------------------------------------------
@st.cache_resource
def load_model(model_path, class_count):
    path = Path(model_path)

    if not path.exists():
        raise FileNotFoundError(f"Model file not found: {path}")

    model = tf.keras.models.load_model(str(path), compile=False)

    if model.input_shape != (None, 224, 224, 3):
        raise ValueError(
            f"Unexpected input shape for {path.name}: {model.input_shape}"
        )

    if model.output_shape != (None, class_count):
        raise ValueError(
            f"Unexpected output shape for {path.name}: {model.output_shape}"
        )

    return model


# --------------------------------------------------
# IMAGE PREPROCESSING
# --------------------------------------------------
def preprocess_image(image, preprocessing_type):
    resized_image = image.resize((224, 224)).convert("RGB")
    image_array = np.asarray(resized_image, dtype=np.float32)

    if preprocessing_type == "densenet":
        # Matches the DenseNet201 training preprocessing.
        image_array = image_array / 255.0

    elif preprocessing_type == "resnet":
        # Matches ResNet101 ImageNet preprocessing.
        image_array = tf.keras.applications.resnet.preprocess_input(
            image_array.copy()
        )

    elif preprocessing_type == "efficientnet":
        # EfficientNetB0 has built-in rescaling.
        # Keep pixel values in the 0–255 range.
        pass

    else:
        raise ValueError(
            f"Unknown preprocessing type: {preprocessing_type}"
        )

    return np.expand_dims(image_array, axis=0)


# --------------------------------------------------
# MODEL PREDICTION
# --------------------------------------------------
def predict_with_model(
    image,
    model_name,
    config,
    model_dir,
    class_labels,
):
    model_path = Path(model_dir) / config["filename"]

    model = load_model(str(model_path), len(class_labels))
    image_batch = preprocess_image(image, config["preprocessing"])

    predictions = model.predict(image_batch, verbose=0)
    scores = predictions[0]

    if scores.shape != (len(class_labels),):
        raise ValueError(
            f"Unexpected predictions from {model_name}"
        )

    if not np.all(np.isfinite(scores)):
        raise ValueError(
            f"Non-finite predictions from {model_name}"
        )

    predicted_index = int(np.argmax(scores))

    return {
        "predicted_class": class_labels[predicted_index],
        "confidence": float(scores[predicted_index] * 100),
        "scores": scores,
    }
