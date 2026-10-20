
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "app"))

from database import get_registered_models, save_prediction

CLASS_LABELS = [
    "Actinic keratosis",
    "Atopic Dermatitis",
    "Benign keratosis",
    "Dermatofibroma",
]

def main():
    models = get_registered_models()
    if not models:
        raise RuntimeError("No active models found in the database.")

    # Use an actual registered model ID.
    model = next(
        (m for m in models if m["ModelName"] == "DenseNet201"),
        None,
    )
    if model is None:
        raise RuntimeError("DenseNet201 is not registered as an active model.")

    # Synthetic values ONLY for testing database writes.
    test_scores = {
        "Actinic keratosis": 0.10,
        "Atopic Dermatitis": 0.20,
        "Benign keratosis": 0.60,
        "Dermatofibroma": 0.10,
    }

    prediction_id = save_prediction(
        model_id=model["ModelID"],
        predicted_class="Benign keratosis",
        confidence=60.0,
        scores=test_scores,
        duration_ms=12,
    )

    print("Synthetic database test succeeded.")
    print(f"Prediction ID: {prediction_id}")
    print("Model: DenseNet201")
    print("Test class: Benign keratosis")
    print(f"Class scores saved: {len(test_scores)}")
    print("These are synthetic test values, not an actual model prediction.")

if __name__ == "__main__":
    main()
