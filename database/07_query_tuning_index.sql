
/*
DeepDerma LabOps — Covering Index Demonstration

Previously observed logical reads:
- Before: 14
- After:   2
- Reduction: approximately 85.7%

Elapsed time did not improve in the original test.
Results depend on data, caching, and execution plans.
*/

USE DeepDermaDB;
GO

IF NOT EXISTS
(
    SELECT 1
    FROM sys.indexes
    WHERE name = N'IX_Predictions_Model_CreatedAt_Covering'
      AND object_id = OBJECT_ID(N'dbo.Predictions')
)
BEGIN
    CREATE NONCLUSTERED INDEX
        IX_Predictions_Model_CreatedAt_Covering
    ON dbo.Predictions
    (
        ModelID,
        CreatedAt DESC
    )
    INCLUDE
    (
        PredictedClass,
        ConfidenceScore,
        DurationMs
    );
END;
GO

SET STATISTICS IO ON;
SET STATISTICS TIME ON;

SELECT
    ModelID,
    CreatedAt,
    PredictedClass,
    ConfidenceScore,
    DurationMs
FROM dbo.Predictions
WHERE ModelID = 1
ORDER BY CreatedAt DESC;

SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;
GO
