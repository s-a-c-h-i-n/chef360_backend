-- Create test teble: Customer
CREATE TABLE dbo.Customer(
	CustomerID INT IDENTITY(1,1) NOT NULL,
	FirstName VARCHAR(25) NOT NULL,
	LastName VARCHAR(25) NOT NULL,
	PhoneNumber VARCHAR(15) NOT NULL,
	EmailAddress VARCHAR(25) NULL,
	Priority INT NOT NULL,
	CreateDate DATETIME NOT NULL)ON [PRIMARY]
GO

ALTER TABLE [dbo].[Customer] ADD CONSTRAINT [DF_Customer_CreateDate] 
DEFAULT (GETDATE()) FOR [CreateDate]
GO

INSERT INTO [dbo].[Customer] values ('John', 'High', '613-111-2222', null, 1))
INSERT INTO [dbo].[Customer] values ('Paul', 'Smith', '613-222-4444', null, 2)