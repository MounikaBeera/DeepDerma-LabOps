
import sys
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

# Make the app folder importable when pytest runs from the project root.
APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

import model_service


@pytest.fixture
def sample_image():
    """Create a small RGB image without needing an external image file."""
    return Image.new("RGB", (100, 80), color=(128, 64, 255))


# --------------------------------------------------
# IMAGE PREPROCESSING TESTS
# --------------------------------------------------

@pytest.mark.parametrize(
    "preprocessing_type",
    ["densenet", "resnet", "efficientnet"],
)
def test_preprocess_image_shape(sample_image, preprocessing_type):
    result = model_service.preprocess_image(
        sample_image, preprocessing_type
    )

    assert result.shape == (1, 224, 224, 3)
    assert result.dtype == np.float32
    assert np.all(np.isfinite(result))


def test_densenet_preprocessing_scales_pixels(sample_image):
    result = model_service.preprocess_image(sample_image, "densenet")

    assert result.min() >= 0.0
    assert result.max() <= 1.0


def test_efficientnet_keeps_pixel_range(sample_image):
    result = model_service.preprocess_image(
        sample_image, "efficientnet"
    )

    assert result.min() >= 0.0
    assert result.max() <= 255.0


def test_unknown_preprocessing_raises_error(sample_image):
    with pytest.raises(ValueError, match="Unknown preprocessing type"):
        model_service.preprocess_image(sample_image, "unknown")


# --------------------------------------------------
# PREDICTION TESTS
# --------------------------------------------------

class FakeModel:
    """A lightweight stand-in for a trained Keras model."""

    def __init__(self, predictions):
        self.predictions = np.asarray(predictions, dtype=np.float32)
        self.received_batch = None

    def predict(self, batch, verbose=0):
        self.received_batch = batch
        return self.predictions


def test_prediction_returns_expected_class_and_scores(
    sample_image, monkeypatch, tmp_path
):
    labels = [
        "Actinic keratosis",
        "Atopic Dermatitis",
        "Benign keratosis",
        "Dermatofibroma",
    ]

    fake_model = FakeModel([[0.1, 0.2, 0.6, 0.1]])

    monkeypatch.setattr(
        model_service, "load_model", lambda *args: fake_model
    )

    config = {
        "filename": "fake_model.keras",
        "preprocessing": "densenet",
    }

    result = model_service.predict_with_model(
        image=sample_image,
        model_name="TestModel",
        config=config,
        model_dir=tmp_path,
        class_labels=labels,
    )

    assert result["predicted_class"] == "Benign keratosis"
    assert result["confidence"] == pytest.approx(60.0)
    np.testing.assert_allclose(
        result["scores"], [0.1, 0.2, 0.6, 0.1], atol=1e-6
    )
    assert fake_model.received_batch.shape == (1, 224, 224, 3)


def test_prediction_rejects_wrong_output_shape(
    sample_image, monkeypatch, tmp_path
):
    fake_model = FakeModel([[0.2, 0.8]])

    monkeypatch.setattr(
        model_service, "load_model", lambda *args: fake_model
    )

    with pytest.raises(ValueError, match="Unexpected predictions"):
        model_service.predict_with_model(
            image=sample_image,
            model_name="TestModel",
            config={
                "filename": "fake_model.keras",
                "preprocessing": "densenet",
            },
            model_dir=tmp_path,
            class_labels=["Class A", "Class B", "Class C", "Class D"],
        )


def test_prediction_rejects_non_finite_scores(
    sample_image, monkeypatch, tmp_path
):
    fake_model = FakeModel([[0.1, np.nan, 0.3, 0.6]])

    monkeypatch.setattr(
        model_service, "load_model", lambda *args: fake_model
    )

    with pytest.raises(ValueError, match="Non-finite predictions"):
        model_service.predict_with_model(
            image=sample_image,
            model_name="TestModel",
            config={
                "filename": "fake_model.keras",
                "preprocessing": "densenet",
            },
            model_dir=tmp_path,
            class_labels=["Class A", "Class B", "Class C", "Class D"],
        )

def test_load_model_rejects_missing_file(tmp_path):
    missing_path = tmp_path / "missing_model.keras"

    with pytest.raises(FileNotFoundError, match="Model file not found"):
        model_service.load_model.__wrapped__(
            str(missing_path), 4
        )


def test_load_model_rejects_wrong_input_shape(monkeypatch, tmp_path):
    model_path = tmp_path / "fake_model.keras"
    model_path.touch()

    class WrongInputModel:
        input_shape = (None, 128, 128, 3)
        output_shape = (None, 4)

    monkeypatch.setattr(
        model_service.tf.keras.models,
        "load_model",
        lambda *args, **kwargs: WrongInputModel(),
    )

    with pytest.raises(ValueError, match="Unexpected input shape"):
        model_service.load_model.__wrapped__(str(model_path), 4)


def test_load_model_rejects_wrong_output_shape(monkeypatch, tmp_path):
    model_path = tmp_path / "fake_model.keras"
    model_path.touch()

    class WrongOutputModel:
        input_shape = (None, 224, 224, 3)
        output_shape = (None, 3)

    monkeypatch.setattr(
        model_service.tf.keras.models,
        "load_model",
        lambda *args, **kwargs: WrongOutputModel(),
    )

    with pytest.raises(ValueError, match="Unexpected output shape"):
        model_service.load_model.__wrapped__(str(model_path), 4)
