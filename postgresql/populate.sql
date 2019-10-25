INSERT INTO Groups VALUES('KM-61');
INSERT INTO Groups VALUES('KM-62');
INSERT INTO Groups VALUES('KM-63');
INSERT INTO Groups VALUES('KM-64');

INSERT INTO Subjects VALUES('Math');
INSERT INTO Subjects VALUES('English');
INSERT INTO Subjects VALUES('Ukrainian');
INSERT INTO Subjects VALUES('Turkish');

INSERT INTO Students VALUES('Volodymyr', 'Drapak', 'KM6103', 'TBD', 'TBD', 'KM-61');
INSERT INTO Students VALUES('Random', 'Guy', 'KM6200', 'TBD', 'TBD', 'KM-62');
INSERT INTO Students VALUES('Always', 'Absent', 'KM6250', 'bad', 'otchislen', 'KM-63');

INSERT INTO SubjectSheet VALUES('Math', 'KM-61', 'KM6103', TO_DATE('28.10.19', 'DD.MM.YY'), 100);
INSERT INTO SubjectSheet VALUES('English', 'KM-61', 'KM6103', TO_DATE('21.10.19', 'DD.MM.YY'), 100);
INSERT INTO SubjectSheet VALUES('Ukrainian', 'KM-61', 'KM6103', TO_DATE('21.10.19', 'DD.MM.YY'), -200);


UPDATE Groups
SET code = 'KM-64r'
WHERE code = 'KM-64';
UPDATE Groups
SET code = 'KM-64m'
WHERE code = 'KM-64r';
UPDATE Groups
SET code = 'KM-71'
WHERE code = 'KM-64m';

UPDATE Subjects
SET name = 'Polish'
WHERE name = 'Turkish';
UPDATE Subjects
SET name = 'Paperwork'
WHERE name = 'Polish';
UPDATE Subjects
SET name = 'DB'
WHERE name = 'Paperwork';

UPDATE Students
SET group_code = 'KM-71'
WHERE destiny = 'otchislen';
UPDATE Students
SET destiny = 'scholarship'
WHERE first_name = 'Volodymyr' AND last_name = 'Drapak';
UPDATE Students
SET group_code = 'KM-62'
WHERE first_name = 'Volodymyr' AND last_name = 'Drapak';

UPDATE SubjectSheet
SET mark = 110
WHERE study_book = 'KM6103';
UPDATE SubjectSheet
SET mark = 120
WHERE study_book = 'KM6103';
UPDATE SubjectSheet
SET mark = 100
WHERE study_book = 'KM6103';


SELECT * FROM Groups;
SELECT * FROM Subjects;
SELECT * FROM Students;
SELECT * FROM SubjectSheet;


DELETE FROM SubjectSheet
WHERE group_code = 'KM-61';
DELETE FROM SubjectSheet
WHERE group_code = 'KM-62';
DELETE FROM SubjectSheet;

DELETE FROM Students
WHERE group_code = 'KM-61';
DELETE FROM Students
WHERE group_code = 'KM-62';
DELETE FROM Students;

DELETE FROM Groups
WHERE code = 'KM-61';
DELETE FROM Groups
WHERE code = 'KM-62';
DELETE FROM Groups;

DELETE FROM Subjects
WHERE name = 'Ukrainian';
DELETE FROM Subjects
WHERE name = 'English';
DELETE FROM Subjects
WHERE name = 'History';
DELETE FROM Subjects;