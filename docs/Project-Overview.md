# DeepDerma-LabOps

## SQL Server Database Administration and Recovery Project

DeepDerma-LabOps combines a multi-model skin-image classification application with SQL Server database administration practices. The project demonstrates database design, controlled application access, query optimization, backup automation, and point-in-time recovery validation.

## Project components

### 1. Application and model comparison

- Streamlit-based interface for comparing three image-classification models.
- Model outputs and class scores presented for the supported classes.
- Python integration with SQL Server for application data persistence.

### 2. SQL Server database

- Database: `DeepDermaDB`
- Structured tables for models, experiments, predictions, prediction scores, and audit events.
- Application login and database user configured with restricted permissions.
- Object-level access controls and denial of table creation for the application user.

### 3. Query optimization

- Tested a covering index on prediction data.
- Logical reads for the tested query decreased from 14 to 2.
- The test also eliminated a key lookup.
- A measurable elapsed-time improvement was not established with the small test dataset.

### 4. Backup and recovery

- Full, differential, and transaction-log backup automation.
- Transaction-log backups scheduled every 15 minutes.
- SQL Server Agent job for point-in-time recovery validation.
- Recovery tested against a separate validation database rather than the production database.

### 5. Recovery validation evidence

The tested recovery target was October 20, 2026, at 5:10 PM.

- SQL Server Agent restore job completed successfully.
- Five table counts matched expected values.
- `DBCC CHECKDB` completed successfully.
- The production database was not used as the restore target.

### 6. Retention safeguards

- Read-only PowerShell backup inventory report.
- Existing cleanup job remains in preview-only mode.
- Backup files are not approved for deletion based on age alone.
- Seven-day recoverable history remains pending verification.

## Technology stack

- Microsoft SQL Server
- SQL Server Management Studio (SSMS)
- T-SQL
- SQL Server Agent
- PowerShell
- Python
- Streamlit

## Current status

The application and database components are implemented, query tuning has been tested, and a point-in-time restore has been validated on a separate database. Backup retention safeguards and final portfolio evidence remain in progress.

## Important limitation

A successful point-in-time restore validates the tested recovery path; it does not prove seven complete days of recoverable history. That coverage must be verified against the actual backup sets and the required recovery chain.

## Learning outcomes

This project demonstrates practical experience with SQL Server security, backup administration, recovery validation, query tuning, PowerShell automation, and technical documentation.
