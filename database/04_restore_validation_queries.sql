
-- Check the database state.
SELECT name, state_desc, recovery_model_desc
FROM sys.databases
WHERE name IN (
    N'DeepDermaDB',
    N'DeepDermaDB_LogRestoreTest'
);
GO

-- Check integrity of the restored test database.
DBCC CHECKDB (N'DeepDermaDB_LogRestoreTest')
WITH NO_INFOMSGS;
GO

-- Compare row counts.
SELECT
    N'Original' AS DatabaseName,
    (SELECT COUNT_BIG(*) FROM DeepDermaDB.dbo.Models) AS Models,
    (SELECT COUNT_BIG(*) FROM DeepDermaDB.dbo.Experiments) AS Experiments,
    (SELECT COUNT_BIG(*) FROM DeepDermaDB.dbo.Predictions) AS Predictions,
    (SELECT COUNT_BIG(*) FROM DeepDermaDB.dbo.PredictionScores)
        AS PredictionScores,
    (SELECT COUNT_BIG(*) FROM DeepDermaDB.dbo.AuditEvents) AS AuditEvents
UNION ALL
SELECT
    N'LogRestoreTest',
    (SELECT COUNT_BIG(*) FROM DeepDermaDB_LogRestoreTest.dbo.Models),
    (SELECT COUNT_BIG(*) FROM DeepDermaDB_LogRestoreTest.dbo.Experiments),
    (SELECT COUNT_BIG(*) FROM DeepDermaDB_LogRestoreTest.dbo.Predictions),
    (SELECT COUNT_BIG(*) FROM DeepDermaDB_LogRestoreTest.dbo.PredictionScores),
    (SELECT COUNT_BIG(*) FROM DeepDermaDB_LogRestoreTest.dbo.AuditEvents);
GO
