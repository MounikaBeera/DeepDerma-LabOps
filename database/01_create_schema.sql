
USE DeepDermaDB;
GO

-- 1. Model registry
CREATE TABLE dbo.Models
(
    ModelID          INT IDENTITY(1,1) PRIMARY KEY,
    ModelName        NVARCHAR(100) NOT NULL UNIQUE,
    FileName         NVARCHAR(260) NOT NULL,
    SHA256Hash       CHAR(64) NULL,
    Preprocessing    NVARCHAR(30) NOT NULL,
    ModelVersion     NVARCHAR(50) NULL,
    IsActive         BIT NOT NULL
        CONSTRAINT DF_Models_IsActive DEFAULT (1),
    CreatedAt        DATETIME2(0) NOT NULL
        CONSTRAINT DF_Models_CreatedAt DEFAULT (SYSUTCDATETIME()),

    CONSTRAINT CK_Models_Preprocessing
        CHECK (Preprocessing IN
            (N'densenet', N'resnet', N'efficientnet'))
);

-- 2. Experiments / analysis sessions
CREATE TABLE dbo.Experiments
(
    ExperimentID     BIGINT IDENTITY(1,1) PRIMARY KEY,
    ExperimentName   NVARCHAR(150) NOT NULL,
    Notes            NVARCHAR(1000) NULL,
    Status           NVARCHAR(20) NOT NULL
        CONSTRAINT DF_Experiments_Status DEFAULT (N'Completed'),
    StartedAt        DATETIME2(0) NOT NULL
        CONSTRAINT DF_Experiments_StartedAt DEFAULT (SYSUTCDATETIME()),

    CONSTRAINT CK_Experiments_Status
        CHECK (Status IN
            (N'Running', N'Completed', N'Failed'))
);

-- 3. One record per model prediction
CREATE TABLE dbo.Predictions
(
    PredictionID     BIGINT IDENTITY(1,1) PRIMARY KEY,
    ExperimentID     BIGINT NULL,
    ModelID          INT NOT NULL,
    PredictedClass   NVARCHAR(100) NOT NULL,
    ConfidenceScore  DECIMAL(9,6) NOT NULL,
    DurationMs       INT NULL,
    CreatedAt        DATETIME2(0) NOT NULL
        CONSTRAINT DF_Predictions_CreatedAt
        DEFAULT (SYSUTCDATETIME()),

    CONSTRAINT FK_Predictions_Models
        FOREIGN KEY (ModelID)
        REFERENCES dbo.Models(ModelID),

    CONSTRAINT FK_Predictions_Experiments
        FOREIGN KEY (ExperimentID)
        REFERENCES dbo.Experiments(ExperimentID),

    CONSTRAINT CK_Predictions_Confidence
        CHECK (ConfidenceScore >= 0 AND ConfidenceScore <= 100),

    CONSTRAINT CK_Predictions_Duration
        CHECK (DurationMs IS NULL OR DurationMs >= 0)
);

-- 4. Four class scores per prediction (when available)
CREATE TABLE dbo.PredictionScores
(
    PredictionID     BIGINT NOT NULL,
    ClassLabel       NVARCHAR(100) NOT NULL,
    Score            DECIMAL(12,10) NOT NULL,

    CONSTRAINT PK_PredictionScores
        PRIMARY KEY (PredictionID, ClassLabel),

    CONSTRAINT FK_PredictionScores_Predictions
        FOREIGN KEY (PredictionID)
        REFERENCES dbo.Predictions(PredictionID)
        ON DELETE CASCADE,

    CONSTRAINT CK_PredictionScores_Range
        CHECK (Score >= 0 AND Score <= 1)
);

-- 5. Application audit / error events
CREATE TABLE dbo.AuditEvents
(
    AuditEventID     BIGINT IDENTITY(1,1) PRIMARY KEY,
    EventType        NVARCHAR(50) NOT NULL,
    EventStatus      NVARCHAR(20) NOT NULL,
    Details          NVARCHAR(1000) NULL,
    CreatedAt        DATETIME2(0) NOT NULL
        CONSTRAINT DF_AuditEvents_CreatedAt
        DEFAULT (SYSUTCDATETIME()),

    CONSTRAINT CK_AuditEvents_Status
        CHECK (EventStatus IN
            (N'Success', N'Failure', N'Warning', N'Info'))
);
GO

-- Indexes for common relationship and history queries
CREATE INDEX IX_Predictions_Model_CreatedAt
    ON dbo.Predictions (ModelID, CreatedAt DESC);

CREATE INDEX IX_Predictions_ExperimentID
    ON dbo.Predictions (ExperimentID);

CREATE INDEX IX_AuditEvents_CreatedAt
    ON dbo.AuditEvents (CreatedAt DESC);
GO
