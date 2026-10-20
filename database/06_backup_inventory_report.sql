
/*
DeepDerma LabOps — Backup Inventory Report
Reports SQL Server backup history; it does not prove that
the backup files currently exist or can be restored.
*/

USE msdb;
GO

SELECT
    bs.database_name,
    CASE bs.type
        WHEN 'D' THEN 'Full'
        WHEN 'I' THEN 'Differential'
        WHEN 'L' THEN 'Transaction Log'
        ELSE bs.type
    END AS backup_type,
    bs.backup_start_date,
    bs.backup_finish_date,
    bs.backup_size / 1048576.0 AS backup_size_mb,
    bs.first_lsn,
    bs.last_lsn,
    bs.checkpoint_lsn,
    bs.database_backup_lsn,
    bmf.physical_device_name
FROM dbo.backupset AS bs
LEFT JOIN dbo.backupmediafamily AS bmf
    ON bs.media_set_id = bmf.media_set_id
WHERE bs.database_name = N'DeepDermaDB'
ORDER BY bs.backup_finish_date DESC;
GO
