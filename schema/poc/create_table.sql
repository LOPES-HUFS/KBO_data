/*PlayerID*/
CREATE TABLE PlayerID (
    playerid INT(10) NOT NULL , 
    playername VARCHAR(30),
    PRIMARY KEY (playerid));

/*scoreboards*/
CREATE TABLE `scoreboard` (
  `idx` bigint(11) NOT NULL,
  `team` varchar(3) DEFAULT NULL,
  `result` int(1) DEFAULT NULL,
  `i_1` int(2) DEFAULT NULL,
  `i_2` int(2) DEFAULT NULL,
  `i_3` int(2) DEFAULT NULL,
  `i_4` int(2) DEFAULT NULL,
  `i_5` int(2) DEFAULT NULL,
  `i_6` int(2) DEFAULT NULL,
  `i_7` int(2) DEFAULT NULL,
  `i_8` int(2) DEFAULT NULL,
  `i_9` int(2) DEFAULT NULL,
  `i_10` int(2) DEFAULT NULL,
  `i_11` int(2) DEFAULT NULL,
  `i_12` int(2) DEFAULT NULL,
  `i_13` int(2) DEFAULT NULL,
  `i_14` int(2) DEFAULT NULL,
  `i_15` int(2) DEFAULT NULL,
  `i_16` int(2) DEFAULT NULL,
  `i_17` int(2) DEFAULT NULL,
  `i_18` int(2) DEFAULT NULL,
  `r` int(2) DEFAULT NULL,
  `h` int(2) DEFAULT NULL,
  `e` int(2) DEFAULT NULL,
  `b` int(2) DEFAULT NULL,
  `year` int(4) DEFAULT NULL,
  `month` int(2) DEFAULT NULL,
  `day` int(2) DEFAULT NULL,
  `week` int(1) DEFAULT NULL,
  `home` varchar(3) DEFAULT NULL,
  `away` varchar(3) DEFAULT NULL,
  `dbheader` int(1) DEFAULT NULL,
  PRIMARY KEY (`idx`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
