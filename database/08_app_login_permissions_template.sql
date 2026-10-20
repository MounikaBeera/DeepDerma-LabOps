
/*
DeepDerma LabOps — Application Login and Least Privilege

Replace the password placeholder securely before execution.
Do not store real credentials in Git.
Review app/database.py to determine the exact permissions required.
*/

USE master;
GO

-- Run only if the application login does not already exist.
-- Replace the placeholder with a strong, unique password.
-- Prefer a secure deployment process for supplying credentials.

-- CREATE LOGIN [DeepDermaAppLogin]
-- WITH PASSWORD = N'<REPLACE_WITH_SECURE_PASSWORD>';
-- GO

USE DeepDermaDB;
GO

-- Run only if the database user does not already exist.
-- CREATE USER [DeepDermaAppUser]
-- FOR LOGIN [DeepDermaAppLogin];
-- GO

-- Confirmed object-level permission from the project:
GRANT SELECT ON OBJECT::dbo.AuditEvents
TO DeepDermaAppUser;
GO

-- Keep permissions limited to the operations the app requires.
-- Do not grant db_owner or broad server-level privileges
-- simply to make connection errors disappear.
