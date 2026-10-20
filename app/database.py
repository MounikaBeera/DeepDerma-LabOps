
import os

import pyodbc


SERVER = r".\DEEPDERMA"
DATABASE = "DeepDermaDB"
DRIVER = "ODBC Driver 18 for SQL Server"
APP_LOGIN = "DeepDermaAppLogin"


def get_connection():
    """Open a connection using the dedicated application login."""
    password = os.environ.get("DEEPDERMA_DB_PASSWORD")

    if not password:
        raise RuntimeError(
            "DEEPDERMA_DB_PASSWORD environment variable is not set."
        )

    connection_string = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={APP_LOGIN};"
        f"PWD={{{password}}};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=10;"
    )

    return pyodbc.connect(connection_string)


def get_registered_models():
    """Retrieve the registered models from SQL Server."""
    query = """
        SELECT
            ModelID,
            ModelName,
            FileName,
            Preprocessing,
            ModelVersion,
            SHA256Hash,
            IsActive
        FROM dbo.Models
        WHERE IsActive = 1
        ORDER BY ModelName;
    """

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query)

        columns = [column[0] for column in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

def create_experiment(experiment_name, notes=None):
    """Create an experiment and return its ID."""
    query = """
        INSERT INTO dbo.Experiments
            (ExperimentName, Notes, Status)
        OUTPUT INSERTED.ExperimentID
        VALUES (?, ?, 'Running');
    """

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, experiment_name, notes)
        experiment_id = cursor.fetchone()[0]
        connection.commit()
        return experiment_id

def record_audit_event(event_type, event_status, details=None):
    """Insert an application audit event using parameterized SQL."""
    query = """
        INSERT INTO dbo.AuditEvents
            (EventType, EventStatus, Details)
        VALUES (?, ?, ?);
    """

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            query,
            event_type,
            event_status,
            details,
        )
        connection.commit()

def save_prediction(
    model_id,
    predicted_class,
    confidence,
    scores,
    duration_ms=None,
    experiment_id=None,
):
    """Save a prediction and its class scores atomically.

    scores must map each class label to its raw model score,
    e.g. {"Actinic keratosis": 0.1, ...}.
    confidence is expressed as a percentage from 0 to 100.
    """
    if not scores:
        raise ValueError("At least one class score is required.")

    if not 0 <= confidence <= 100:
        raise ValueError("Confidence must be between 0 and 100.")

    if duration_ms is not None and duration_ms < 0:
        raise ValueError("Duration cannot be negative.")

    prediction_query = """
        INSERT INTO dbo.Predictions
            (ExperimentID, ModelID, PredictedClass,
             ConfidenceScore, DurationMs)
        OUTPUT INSERTED.PredictionID
        VALUES (?, ?, ?, ?, ?);
    """

    score_query = """
        INSERT INTO dbo.PredictionScores
            (PredictionID, ClassLabel, Score)
        VALUES (?, ?, ?);
    """

    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            prediction_query,
            experiment_id,
            model_id,
            predicted_class,
            confidence,
            duration_ms,
        )

        prediction_id = cursor.fetchone()[0]

        score_rows = [
            (prediction_id, label, float(score))
            for label, score in scores.items()
        ]

        cursor.executemany(score_query, score_rows)
        connection.commit()

        return prediction_id

def update_experiment_status(experiment_id, status):
    """Update an experiment's status."""
    if status not in {"Running", "Completed", "Failed"}:
        raise ValueError("Invalid experiment status.")

    query = """
        UPDATE dbo.Experiments
        SET Status = ?
        WHERE ExperimentID = ?;
    """

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, status, experiment_id)

        if cursor.rowcount == 0:
            raise ValueError(
                f"Experiment {experiment_id} was not found."
            )

        connection.commit()

def get_model_id(model_name):
    """Return the registered ModelID for an active model."""
    query = """
        SELECT ModelID
        FROM dbo.Models
        WHERE ModelName = ? AND IsActive = 1;
    """
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, model_name)
        row = cursor.fetchone()
        return row[0] if row else None
