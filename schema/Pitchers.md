## Patters

투수들의 정보를 담은 테이블

### schema

```sql

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

### Info

- idx: scoreboards의 외래키, 경기정보와 연결되어 있다.
- playerid: PlayerID의 외래키, 선수의 이름과 연결되어 있다.
- position: 특정 경기에서 해당 선수가 맡은 역할을 코드로 바꾸어 저장한다. 코드로 바꾸는 이유는 한자를 대체하기 위해서이다. 


## playerid

각 선수들의 아이디와 이름을 매칭하는 테이블, 개명하는 선수들이 존재하기에 이름을 하나의 테이블로 관리한다.

### schema

```sql
playerid = Column(Integer)
name = Column(String(20))
```
