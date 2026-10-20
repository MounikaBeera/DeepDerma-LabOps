
/*
DeepDerma-LabOps
Manual SQL Server backup examples.

Replace the date placeholders with unique filenames.
Ensure the SQL Server service account can write to the backup directory.
*/

USE master;
GO

-- 1. Full backup
BACKUP DATABASE [DeepDermaDB]
TO DISK = N'D:\SQLBackups\DeepDermaDB_Full_REPLACE_DATE.bak'
WITH INIT, CHECKSUM, STATS = 10;
GO

-- 2. Differential backup
BACKUP DATABASE [DeepDermaDB]
TO DISK = N'D:\SQLBackups\DeepDermaDB_Diff_REPLACE_DATE.bak'
WITH DIFFERENTIAL, INIT, CHECKSUM, STATS = 10;
GO

-- 3. Transaction log backup
-- Requires FULL recovery and an established log-backup chain.
BACKUP LOG [DeepDermaDB]
TO DISK = N'D:\SQLBackups\DeepDermaDB_Log_REPLACE_DATE.trn'
WITH INIT, CHECKSUM, STATS = 10;
GO
