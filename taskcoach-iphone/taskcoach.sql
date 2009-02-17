
-- Status is:

-- 0: None
-- 1: new
-- 2: modified
-- 3: deleted

CREATE TABLE Category
(
	id INTEGER PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	status INTEGER NOT NULL DEFAULT 1,
	taskCoachId VARCHAR(255) NULL DEFAULT NULL,
	parentTaskCoachId VARCHAR(255) NULL DEFAULT NULL
);

CREATE INDEX idxCategoryStatus ON Category (status);
CREATE INDEX idxCategoryName ON Category (name);
CREATE INDEX idxCategoryTaskCoachId ON Category (taskcoachId);

CREATE TABLE Task
(
	id INTEGER PRIMARY KEY,
	name VARCHAR(2048) NOT NULL,
	status INTEGER NOT NULL DEFAULT 1,
	taskCoachId VARCHAR(255) NULL DEFAULT NULL,

	-- Task-specific fields

	description TEXT NOT NULL DEFAULT '',
	
	-- Dates are represented as YYYY-MM-DD strings
	
	startDate CHAR(10) NULL DEFAULT NULL,
	dueDate CHAR(10) NULL DEFAULT NULL,
	completionDate CHAR(10) NULL DEFAULT NULL
);

CREATE INDEX idxTaskStatus ON Task (status);
CREATE INDEX idxTaskName ON Task (name);
CREATE INDEX idxTaskTaskCoachId ON Task (taskcoachId);

CREATE TABLE TaskHasCategory
(
	idTask INTEGER,
	idCategory INTEGER
);

CREATE INDEX idxTaskHasCategoryTask ON TaskHasCategory (idTask);
CREATE INDEX idxTaskHasCategoryCategory ON TaskHasCategory (idCategory);

CREATE TABLE Meta
(
	name VARCHAR(255) NOT NULL,
	value VARCHAR(255)
);

CREATE UNIQUE INDEX idxMetaName ON Meta (name);

-- Views

CREATE VIEW AllTask AS SELECT * FROM Task WHERE status != 3 ORDER BY name;
CREATE VIEW OverdueTask AS SELECT * FROM Task WHERE status != 3 AND dueDate < DATE('now') ORDER BY dueDate, startDate DESC;
CREATE VIEW DueTodayTask AS SELECT * FROM Task WHERE status != 3 AND dueDate == DATE('now') ORDER BY startDate DESC;
CREATE VIEW StartedTask AS SELECT * FROM Task WHERE status != 3 AND startDate IS NOT NULL AND startDate <= DATE('now') AND (dueDate > DATE('now') OR dueDate IS NULL) ORDER BY startDate;
CREATE VIEW NotStartedTask AS SELECT * FROM Task WHERE status != 3 AND startDate IS NULL AND (dueDate > DATE('now') OR dueDate IS NULL);

-- Initial data

INSERT INTO Meta (name, value) VALUES ('version', '1');