# DeepDermaDB — Backup Retention Policy

## 1. Purpose

Define a safe retention approach for SQL Server full, differential, and transaction-log backups while preserving the ability to perform point-in-time recovery.

## 2. Backup schedule

| Backup type | Configured schedule |
|---|---|
| Full backup | Daily at 10:00 PM |
| Differential backup | Daily at 11:00 PM |
| Transaction-log backup | Every 15 minutes |
| Retention preview | Daily at 12:30 AM |

## 3. Retention objective

The target is to maintain seven days of recoverable database history.

Seven-day coverage is not yet verified. The policy must not claim that this target has been achieved until the actual backup files and complete required recovery chain have been validated.

## 4. Safety controls

- The cleanup job remains in preview-only mode.
- Backup files are not deleted based on file age alone.
- Actual backup sets and their recovery dependencies must be verified.
- Historical SQL Server backup records must not be assumed to represent the current contents of a reused filename.
- Existing backup files must remain untouched until the retention decision is validated.
- Recovery validation must be performed on a separate test database.

## 5. Retention review process

1. Inventory the existing backup files.
2. Identify the backup sets actually present in each file.
3. Confirm the full backup and any selected differential backup are compatible.
4. Confirm the required transaction-log backups provide a continuous recovery path.
5. Confirm the oldest required recovery point is covered.
6. Test the intended restore path before approving a cleanup policy.
7. Keep the cleanup job in preview-only mode until these checks pass.

## 6. Current status

- Backup automation: Configured
- PITR validation: Successful for the tested recovery point
- Read-only file inventory: Implemented
- Dependency-aware retention validation: Pending
- Seven-day recovery coverage: Pending verification
- Automatic backup deletion: Disabled

## 7. Completion criteria

The retention objective is considered validated only after sufficient history exists and the required recovery chain has been confirmed. A successful PITR test at one recovery point does not prove seven days of recoverable history.
