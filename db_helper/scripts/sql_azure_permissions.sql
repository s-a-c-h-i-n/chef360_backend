-- Add azure Entra (AD) user to DB
CREATE USER [user1@uottawa.ca] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [user1@uottawa.ca];
ALTER ROLE db_datawriter ADD MEMBER [user1@uottawa.ca];
ALTER ROLE db_ddladmin ADD MEMBER [user1@uottawa.ca];
GO

-- Check user role to DB
SELECT r.name role_principal_name, 
       m.name AS member_principal_name
  FROM sys.database_role_members rm 
  JOIN sys.database_principals r 
       ON rm.role_principal_id = r.principal_id
  JOIN sys.database_principals m 
       ON rm.member_principal_id = m.principal_id
 WHERE r.type = 'R';