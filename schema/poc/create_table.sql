/*teamID*/
CREATE TABLE TeamID (
    teamid INT(3) NOT NULL , 
    teamname VARCHAR(10),
     PRIMARY KEY (teamid));

/*PlayerID*/
CREATE TABLE PlayerID (
    playerid INT(10) NOT NULL , 
    playername VARCHAR(30),
     PRIMARY KEY (playerid));

/*scoreboards*/
CREATE TABLE scoreboards(
    idx INT(15) NOT NULL,
    PRIMARY KEY (idx),
    teamid INT NOT NULL,
    year INT(4) NOT NULL,
    month INT(3) NOT NULL,
    day INT(3) NOT NULL,
    CONSTRAINT TeamID_teamid_fk FOREIGN KEY (teamid) REFERENCES TeamID (teamid)
);

/*batters*/
CREATE TABLE batters(
    idx INT NOT NULL,
    playerid INT NOT NULL,
    position VARCHAR(20) NOT NULL,
    batnum INT(10) NOT NULL,
    hit INT(10) NOT NULL,
    CONSTRAINT scoreboards_batteridx_fk FOREIGN KEY (idx) REFERENCES scoreboards (idx),
    CONSTRAINT PlayerID_batter_fk FOREIGN KEY (playerid) REFERENCES PlayerID (playerid)
);


/*pitchers*/
CREATE TABLE pitchers(
    idx INT NOT NULL,
    playerid INT NOT NULL,
    position VARCHAR(20) NOT NULL,
    inning INT(10) NOT NULL,
    rest INT(10) NOT NULL,
    CONSTRAINT scoreboards_pitcheridx_fk FOREIGN KEY (idx) REFERENCES scoreboards (idx),
    CONSTRAINT PlayerID_pitcher_fk FOREIGN KEY (playerid) REFERENCES PlayerID (playerid)
);