
/*
DeepDerma LabOps — Point-in-Time Recovery (PITR)

Prerequisites:
1. Verify the full backup and any required differential backup.
2. Verify every transaction-log backup in sequence.
3. Confirm the target time is covered by the log chain.
4. Use a separate validation database, never overwrite production
   during a portfolio recovery exercise.

Recovery sequence:
- Restore FULL backup WITH NORECOVERY.
- Optionally restore a compatible DIFFERENTIAL WITH NORECOVERY.
- Restore each required LOG backup in sequence WITH NORECOVERY.
- Apply STOPAT to the final log restore.
- Restore the final log WITH RECOVERY.

Example syntax only — replace paths and time before execution:

RESTORE DATABASE [DeepDermaDB_PITR_Validation]
FROM DISK = N'D:\SQLBackups\REPLACE_FULL_BACKUP.bak'
WITH
    MOVE N'DeepDermaDB' TO
        N'D:\SQLData\DeepDermaDB_PITR_Validation.mdf',
    MOVE N'DeepDermaDB_log' TO
        N'D:\SQLData\DeepDermaDB_PITR_Validation_log.ldf',
    NORECOVERY,
    CHECKSUM,
    STATS = 10;

-- If using a differential backup, restore it next with NORECOVERY.
-- Restore every required log backup in sequence.
-- On the final log restore, specify the verified target time:
--
-- RESTORE LOG [DeepDermaDB_PITR_Validation]
-- FROM DISK = N'D:\SQLBackups\REPLACE_FINAL_LOG.trn'
-- WITH STOPAT = 'YYYY-MM-DDTHH:MM:SS',
--      RECOVERY, CHECKSUM, STATS = 10;
--
-- Validate the recovered database using DBCC CHECKDB and row counts.
