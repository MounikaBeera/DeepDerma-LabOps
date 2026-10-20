# DeepDerma LabOps — Setup Guide

## 1. Overview

DeepDerma LabOps combines a Streamlit-based machine-learning application with a Microsoft SQL Server database. This guide describes how to configure a local development environment.

The setup uses Windows, Python, SQL Server, and SQL Server Management Studio (SSMS). Some configuration details vary by installation.

## 2. Prerequisites

Install or prepare the following:

- Windows 10 or Windows 11.
- Python version compatible with the project's dependency files.
- Microsoft SQL Server Developer or another appropriately licensed edition.
- SQL Server Management Studio (SSMS).
- Git.
- A compatible TensorFlow installation and the project's required Python packages.

Check the repository for the current dependency files before installing packages.

## 3. Clone the Repository

Open PowerShell:

```powershell
git clone https://github.com/MounikaBeera/DeepDerma-LabOps.git
cd DeepDerma-LabOps
```

## 4. Configure Python

Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies using the dependency file included in the repository. For example, if `requirements.txt` exists:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If the repository does not contain a dependency file, identify the application's required packages before installing them. TensorFlow compatibility can depend on Python and operating-system versions.

## 5. Configure SQL Server

1. Install and start a SQL Server instance.
2. Open SSMS and connect using an account authorized to create databases and configure permissions.
3. Review `database/01_create_schema.sql` and `database/02_seed_models.sql`.
4. Execute the scripts in the documented order.
5. Verify that the expected tables and seed records exist.

The SQL Server instance name, database name, authentication method, and file paths may differ from the original development environment. Review scripts before executing them.

## 6. Configure Application Credentials

The application reads its SQL Server password from the `DEEPDERMA_DB_PASSWORD` environment variable.

Set it for the current PowerShell session without placing the password in the command history:

```powershell
$securePassword = Read-Host "SQL Server application password" -AsSecureString
$pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)

try {
    $env:DEEPDERMA_DB_PASSWORD =
        [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)

    # Launch the application in this session.
    # Replace this command if the repository's entry point differs.
    streamlit run app.py
}
finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
    Remove-Item Env:DEEPDERMA_DB_PASSWORD -ErrorAction SilentlyContinue
    $securePassword.Dispose()
}
```

This example supplies the password through the environment. It does not configure the application's server, database name, or authentication settings. Review `app/database.py` and configure those settings for your own SQL Server instance.

Do not commit real credentials to GitHub.

## 7. Launch the Application

From the activated virtual environment, run:

```powershell
streamlit run app.py
```

Open the local address printed by Streamlit in the terminal.

If your repository provides `run_app.ps1`, review its contents first. Replace any machine-specific Python paths and verify that it handles credentials safely before using it.

## 8. Backup and Recovery Labs

Review these scripts before running them:

- `database/03_manual_backup_full_diff_log.sql`
- `database/04_restore_validation_queries.sql`
- `database/05_point_in_time_restore.sql`
- `database/06_backup_inventory_report.sql`

The backup and recovery scripts contain environment-specific paths or placeholders. Confirm the SQL Server service account has access to backup directories, verify the backup chain, and use a separate validation database for restore exercises.

Do not run a recovery template unchanged against a production database.

## 9. Troubleshooting

### SQL Server connection failure

- Verify the instance name and that the SQL Server service is running.
- Check authentication mode and login permissions.
- Confirm the database name and network configuration.
- Check that the application is reading the expected connection settings.

### Login or permission errors

- Confirm the login and database user exist.
- Review the grants required by the application's actual SQL statements.
- Avoid granting broad administrative roles just to bypass an error.

### Missing Python packages

- Activate the intended virtual environment.
- Confirm the Python version is compatible with the project's dependencies.
- Install packages from the repository's dependency file, if available.

### Backup or restore failure

- Check the backup path and SQL Server service-account permissions.
- Verify backup metadata and log-chain continuity.
- Confirm logical file names and physical paths before using `MOVE`.
- Restore into a dedicated validation database.

## 10. Security Notes

- Never publish passwords, connection secrets, or private keys.
- Use a dedicated application login with least-privilege permissions.
- Keep development and production environments separate.
- Verify backup recoverability instead of relying only on backup-history records.
- Review all SQL scripts before executing them.

## 11. Project Limitations

This guide is a starting point for a local Windows development setup. SQL Server configuration, model files, dependency versions, and application settings may require adjustment for a different machine. Successful setup should be confirmed by running the application and validating the database connection.
