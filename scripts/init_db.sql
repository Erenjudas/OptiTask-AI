IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'OptiTaskDB')
BEGIN
    CREATE DATABASE OptiTaskDB;
END
GO

USE OptiTaskDB;
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Tasks')
BEGIN
    CREATE TABLE Tasks (
        TaskID INT PRIMARY KEY IDENTITY(1,1),
        Name NVARCHAR(255) NOT NULL,
        Deadline INT NOT NULL,         -- days left
        Difficulty INT NOT NULL,       -- scale 1-5
        Importance INT NOT NULL,       -- scale 1-5
        PriorityScore FLOAT NULL,
        Recommendation NVARCHAR(50) NULL,
        Status NVARCHAR(50) DEFAULT 'Pending',
        UserID INT
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'TaskHistory')
BEGIN
    CREATE TABLE TaskHistory (
        HistoryID INT PRIMARY KEY IDENTITY(1,1),
        TaskID INT FOREIGN KEY REFERENCES Tasks(TaskID),
        Action NVARCHAR(50),           -- Completed / Delayed
        Timestamp DATETIME DEFAULT GETDATE()
    );
END
GO
