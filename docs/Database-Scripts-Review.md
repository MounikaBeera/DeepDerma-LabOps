# Database Scripts Review — DeepDerma LabOps

## Overview

This document describes the SQL Server administration scripts included in DeepDerma LabOps. The scripts demonstrate database backup and recovery, backup-history reporting, query tuning, and application least-privilege security.

## Script Inventory

| File | Purpose |
|---|---|
| `01_create_schema.sql` | Creates the application database schema. |
| `02_seed_models.sql` | Seeds model reference data. |
| `03_manual_backup_full_diff_log.sql` | Demonstrates full, differential, and transaction-log backups. |
| `04_restore_validation_queries.sql` | Provides database integrity and row-count validation queries. |
| `05_point_in_time_restore.sql` | Documents the point-in-time recovery workflow. |
| `06_backup_inventory_report.sql` | Reports backup history recorded in `msdb`. |
| `07_query_tuning_index.sql` | Demonstrates a covering index and query-statistics collection. |
| `08_app_login_permissions_template.sql` | Documents application-login setup and object-level permissions. |

## Backup and Recovery

The project uses SQL Server full, differential, and transaction-log backups. A recovery workflow must use a compatible backup chain, restore backups in the correct order, and apply `STOPAT` only when the target time is covered by the transaction-log backups.

Recovery exercises should use a separate validation database. After restoration, run `DBCC CHECKDB` and verify application table contents.

The scripts contain placeholders where paths, logical file names, backup files, or target recovery times must be confirmed for the local environment.

## Backup Inventory and Retention

The inventory query reads SQL Server backup history from `msdb`. History entries alone do not prove that a backup file still exists or is restorable.

A retention policy should be verified against actual files, backup-chain dependencies, and successful restore tests before old backups are deleted. The seven-day retention window has not been fully verified in this project.

## Query Tuning

The project tested the covering index `IX_Predictions_Model_CreatedAt_Covering`.

In the recorded test, logical reads decreased from 14 to 2—approximately an 85.7% reduction. Elapsed time did not improve in that test, so the result is evidence of reduced logical reads, not proof of a faster query in every environment.

Execution plans, logical reads, elapsed time, index-maintenance overhead, and representative data volumes should all be considered when evaluating a tuning change.

## Application Security

The Streamlit application uses a dedicated SQL Server login and database user. Credentials are supplied through an environment variable rather than embedded in the application source.

The application account should receive only the permissions needed by the application. Avoid broad roles such as `db_owner` unless there is a separately justified administrative requirement.

The login script is a template. Review the application's actual SQL statements and the existing database permissions before applying changes.

## Environment and Safety

- SQL Server instance and local file paths vary by machine.
- The SQL Server service account must have the required access to backup locations.
- The transaction-log backup workflow requires the appropriate recovery model and an established log chain.
- Test backup and recovery procedures in a non-production environment first.
- Do not commit real passwords, access tokens, or other secrets to GitHub.

## Validation Status

The project includes backup and restore exercises, database integrity checks, and table row-count validation. These checks support the lab demonstration but do not guarantee that every historical backup is recoverable or that the retention policy has been fully enforced.

## Reproducibility

Before reproducing the labs, review the SQL files, adapt instance names and paths, verify permissions, and confirm that the backup chain is valid. Record the environment and results of each restore test so that future runs can be compared consistently.
