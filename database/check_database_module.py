
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "app"))

from database import get_registered_models, record_audit_event


def main():
    models = get_registered_models()

    print(f"Registered active models: {len(models)}")

    for model in models:
        print(
            f"- {model['ModelName']} | "
            f"{model['Preprocessing']} | "
            f"Active: {model['IsActive']}"
        )

    record_audit_event(
        "DatabaseModuleTest",
        "Success",
        "Reusable database module connection and query test",
    )

    print("Audit event inserted successfully.")


if __name__ == "__main__":
    main()
