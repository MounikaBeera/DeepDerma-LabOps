
USE DeepDermaDB;
GO

-- Register DenseNet201
IF NOT EXISTS (
    SELECT 1 FROM dbo.Models
    WHERE ModelName = N'DenseNet201'
)
BEGIN
    INSERT INTO dbo.Models
        (ModelName, FileName, Preprocessing, ModelVersion)
    VALUES
        (N'DenseNet201',
         N'densenet201_finetuned_best.keras',
         N'densenet',
         N'finetuned-best');
END;

-- Register ResNet101
IF NOT EXISTS (
    SELECT 1 FROM dbo.Models
    WHERE ModelName = N'ResNet101'
)
BEGIN
    INSERT INTO dbo.Models
        (ModelName, FileName, Preprocessing, ModelVersion)
    VALUES
        (N'ResNet101',
         N'resnet101_finetuned_best.keras',
         N'resnet',
         N'finetuned-best');
END;

-- Register EfficientNetB0
IF NOT EXISTS (
    SELECT 1 FROM dbo.Models
    WHERE ModelName = N'EfficientNetB0'
)
BEGIN
    INSERT INTO dbo.Models
        (ModelName, FileName, Preprocessing, ModelVersion)
    VALUES
        (N'EfficientNetB0',
         N'efficientnetb0_finetuned_best.keras',
         N'efficientnet',
         N'finetuned-best');
END;
GO

SELECT
    ModelID,
    ModelName,
    FileName,
    Preprocessing,
    ModelVersion,
    SHA256Hash,
    IsActive
FROM dbo.Models
ORDER BY ModelID;
GO
