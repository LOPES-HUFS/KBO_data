
```sql
CREATE TABLE pitcher(
    idx BIGINT(11) NOT NULL,
    playerid INT(5) NOT NULL,
    position CHAR(4) DEFAULT NULL,
    join DECIMAL(3,1) DEFAULT NULL,
    inning INT(1) DEFAULT NULL,
    rest INT(1) DEFAULT NULL,
    save TINYINT(1) DEFAULT NULL,
    hold TINYINT(1) DEFAULT NULL,
    strikeout INT(2) DEFAULT NULL,
    dead4ball INT(2) DEFAULT NULL,
    losescore INT(2) DEFAULT NULL,
    earnedrun INT(2) DEFAULT NULL,
    pitchnum INT(3) DEFAULT NULL,
    hitted INT(2) DEFAULT NULL,
    homerun INT(2) DEFAULT NULL,
    battednum INT(2) DEFAULT NULL,
    batternum INT(2) DEFAULT NULL,
    CONSTRAINT scoreboards_pitcher_idx_fk FOREIGN KEY (idx) REFERENCES scoreboard (idx),
    CONSTRAINT player_id_pitcher_playerid_fk FOREIGN KEY (playerid) REFERENCES player_id (playerid)
);
```
