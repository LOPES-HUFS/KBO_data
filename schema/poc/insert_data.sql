/*teamID*/

INSERT INTO TeamID 
VALUES
(1,'SSG'), (2, 'HH'), (3, 'DS');

/*PlayerID*/

INSERT INTO PlayerID 
VALUES
(100,'RHJ'), (200, 'KGD'), (300, 'SEGH');

/*scoreboards*/
INSERT INTO scoreboards
VALUES
(2021050123, 1, 2021, 05, 01),
(2021050211, 2, 2021, 05, 02),
(2021050332, 3, 2021, 05, 03);

/*batters*/
INSERT INTO batters
VALUES
(2021050123, 100, 'left', 3, 2),
(2021050123, 200, 'right', 0, 0),
(2021050123, 300, 'cneter', 2, 1),
(2021050211, 100, 'right', 5, 1),
(2021050211, 300, 'left', 2, 1);

/*pitchers*/
INSERT INTO pitchers
VALUES
(2021050123, 100, 'dont', 3, 2),
(2021050211, 200, 'know', 0, 0),
(2021050211, 100, 'what', 2, 1),
(2021050332, 100, 'type', 5, 1),
(2021050332, 200, 'exist', 2, 1);
