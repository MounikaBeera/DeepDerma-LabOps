
import os
import pyodbc

server = r".\DEEPDERMA"
database = "DeepDermaDB"
username = "DeepDermaAppLogin"
password = os.environ.get("DEEPDERMA_DB_PASSWORD")

if not password:
    raise RuntimeError(
        "Set the DEEPDERMA_DB_PASSWORD environment variable first."
    )

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={{{password}}};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
    "Connection Timeout=10;"
)

with pyodbc.connect(connection_string) as connection:
    cursor = connection.cursor()
    cursor.execute("""
        SELECT
            @@SERVERNAME AS ServerName,
            DB_NAME() AS DatabaseName,
            SUSER_SNAME() AS LoginName,
            COUNT(*) AS RegisteredModels
        FROM dbo.Models;
    """)

    row = cursor.fetchone()

    print("Connection successful!")
    print("Server:", row.ServerName)
    print("Database:", row.DatabaseName)
    print("Login:", row.LoginName)
    print("Registered models:", row.RegisteredModels)
