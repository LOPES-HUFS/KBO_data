## pitchers

투수들의 정보를 담은 테이블

### schema

```sql
CREATE TABLE pitcher(
    idx BIGINT(11) NOT NULL COMMENT "조합키(시합날짜+더블헤더+팀ID)",
    playerid INT(5) NOT NULL COMMENT "선수ID",
    team VARCHAR(4)  DEFAULT NULL COMMENT "팀이름",
    mound TINYINT(1) DEFAULT NULL COMMENT "선발",
    inning INT(1) DEFAULT NULL COMMENT "이닝",
    result VARCHAR(3) DEFAULT NULL COMMENT "결과",
    strikeout INT(2) DEFAULT NULL COMMENT "삼진",
    dead4ball INT(2) DEFAULT NULL COMMENT "4사구",
    losescore INT(2) DEFAULT NULL COMMENT "실점",
    earnedrun INT(2) DEFAULT NULL COMMENT "자책",
    pitchnum INT(3) DEFAULT NULL COMMENT "투구수",
    hitted INT(2) DEFAULT NULL COMMENT "피안타",
    homerun INT(2) DEFAULT NULL COMMENT "피홈런",
    battednum INT(2) DEFAULT NULL COMMENT "피타수",
    batternum INT(2) DEFAULT NULL COMMENT "피타자",
    CONSTRAINT scoreboards_pitcher_idx_fk FOREIGN KEY (idx) REFERENCES scoreboard (idx),
    CONSTRAINT player_id_pitcher_playerid_fk FOREIGN KEY (playerid) REFERENCES player_id (playerid)
);
```

### Info

- idx: scoreboards의 외래키, 경기정보와 연결되어 있다.
- playerid: PlayerID의 외래키, 선수의 이름과 연결되어 있다.
- position: 특정 경기에서 해당 선수가 맡은 역할을 코드로 바꾸어 저장한다. 코드로 바꾸는 이유는 한자를 대체하기 위해서이다.
- saved: 투수들이 ''승리조건''을 지키는 것 (0,1) 우리팀이 이기고 있는 상황에서 경기종료 시까지 선발투수가 아닌 투수가 점수를 빼앗기지 않은 경우
- hold: 등판하고 승리조건을 유지하다가 내려간 투수들을 잘 붙잡고 있었다는 의미로 홀드 줌

## playerid

각 선수들의 아이디와 이름을 매칭하는 테이블, 개명하는 선수들이 존재하기에 이름을 하나의 테이블로 관리한다.
