# DeepDerma LabOps

A SQL Server DBA portfolio project demonstrating database administration, backup and recovery, security, SQL Agent automation, and query performance tuning through a Streamlit-based application.

## Project Overview

DeepDerma LabOps connects a skin-condition image analysis application to Microsoft SQL Server. Alongside the application, the project demonstrates practical DBA workflows for protecting data, managing access, validating recovery, and investigating query performance.

## Technology Stack

- Microsoft SQL Server 2022
- SQL Server Management Studio (SSMS)
- T-SQL
- SQL Server Agent
- Windows PowerShell
- Python and Streamlit
- Git and GitHub

## DBA Work Demonstrated

### Database Security
- SQL logins, database users, roles, and permissions
- Application access configured with restricted permissions
- Password supplied through an environment variable rather than hardcoded in application source

### Backup and Recovery
- Full, differential, and transaction-log backups
- SQL Server Agent jobs for backup automation
- Backup verification using checksums and restore validation
- Point-in-time recovery tested in a separate validation database
- Database integrity checking with `DBCC CHECKDB`

**Recovery note:** Point-in-time recovery was successfully validated for the documented test scenario. The full seven-day retention window has not yet been verified.

### Query Performance
An index-tuning exercise reduced logical reads from 14 to 2 for the tested query, an approximately 85.7% reduction in logical reads. This result is specific to the test workload and does not establish a corresponding improvement in elapsed time.

### Automation and Documentation
- SQL Server Agent backup and validation jobs
- PowerShell launcher for application setup
- Backup retention reporting in preview mode
- Recovery runbook, retention policy, project overview, and supporting screenshots

## Repository Structure

- `app/` — Streamlit application and database integration
- `database/` — SQL schema, seed scripts, and database tests
- `docs/` — DBA documentation and recovery procedures
- `screenshots/` — Evidence of application and DBA validation
- `artifacts/` — Model reference hashes
- `tests/` — Automated tests
- `run_app.ps1` — Local application launcher

## Prerequisites

- Windows
- Python and the dependencies required by the application
- Microsoft SQL Server with the `DeepDermaDB` database and required schema
- The trained model files required by the application

## Setup

1. Clone or download this repository.
2. Review `database/01_create_schema.sql` and `database/02_seed_models.sql` before running the scripts in your SQL Server environment.
3. Configure the application database connection in `app/database.py` for your own SQL Server instance.
4. Set the `DEEPDERMA_DB_PASSWORD` environment variable when launching the application. Do not commit passwords or other secrets.
5. Configure the Python import path in `run_app.ps1` for your environment.
6. Obtain the trained model files separately and place them in the expected `models/` directory. The model files are not included in this repository.
7. Run the launcher from PowerShell:

   ```powershell
   .\run_app.ps1
   ```

The launcher prompts for the SQL application login password when it starts.

## Validation Evidence

The `screenshots/` directory contains supporting evidence for the documented backup jobs, point-in-time recovery, recovered row counts, database integrity check, query tuning, and application interface.

## Important Limitations

- This repository is a learning and portfolio project, not a production-ready medical diagnostic system.
- Image-analysis outputs are for demonstration purposes and must not be used as a substitute for professional medical advice.
- Model files, database credentials, and environment-specific configuration are not included.
- Review and adapt SQL scripts and configuration before using them in another environment.

## Author

**Mounika Beera**

SQL Server DBA portfolio project.
