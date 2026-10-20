# DeepDermaDB — Point-in-Time Recovery Runbook

## 1. Objective

Document the point-in-time recovery (PITR) exercise performed on SQL Server using a separate validation database.

## 2. Environment

- **Database:** `DeepDermaDB`
- **SQL Server instance:** `MOUNIKA\DEEPDERMA`
- **Recovery model:** FULL
- **Backup directory:** `D:\SQLBackups`
- **Validation database:** `DeepDermaDB_PITR_Validation`
- **Production database:** `DeepDermaDB`

## 3. Recovery target

- **Date:** October 20, 2026
- **Target time:** 5:10 PM
- **Method:** Full backup, matching differential backup, sequential transaction-log restores, and `STOPAT`.

## 4. Recovery procedure

1. Restore the full backup using `NORECOVERY`.
2. Restore the matching differential backup using `NORECOVERY`.
3. Restore the required transaction-log backups in sequence using `NORECOVERY`.
4. Apply the final transaction-log restore with `STOPAT = '2026-10-20T17:10:00'`.
5. Use `RECOVERY` to bring the validation database online.
6. Compare recovered table counts against expected values.
7. Run `DBCC CHECKDB` against the validation database.

## 5. Validation results

| Validation | Result |
|---|---|
| SQL Server Agent restore job | Succeeded |
| Restore target | Separate validation database |
| Production database used as restore target | No |
| Models row count | 3 |
| Experiments row count | 4 |
| Predictions row count | 16 |
| PredictionScores row count | 64 |
| AuditEvents row count | 4 |
| Table-count comparison | 5 of 5 matched |
| `DBCC CHECKDB` | Succeeded |

## 6. Backup automation and retention

- Full, differential, and transaction-log backup jobs are configured.
- Transaction-log backups are scheduled every 15 minutes.
- The cleanup job remains preview-only.
- A separate PowerShell report inventories `.bak` and `.trn` files without deleting them.
- Backup dependencies must be verified before any file is approved for deletion.

## 7. Limitations and follow-up

The successful PITR test validates the recovery path that was tested. It does not independently establish seven complete days of recoverable history.

Seven-day coverage remains pending until sufficient backup history and the complete required recovery chain are verified. Keep the cleanup job in preview-only mode until that validation is complete.

## 8. Conclusion

The PITR validation restore completed successfully on a separate database. The restore job, row-count comparison, and database integrity check passed. The production database was not the restore target.

Backup automation is configured, and retention safeguards remain in progress pending verification of the seven-day recovery window.
