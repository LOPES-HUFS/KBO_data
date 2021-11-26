## Batters

타자들의 정보를 담은 테이블

### schema

```sql
CREATE TABLE batter(
    idx BIGINT(11) NOT NULL COMMENT "조합키(시합날짜+더블헤더+팀ID)",
    playerid INT(5) NOT NULL COMMENT "선수ID",
    position VARCHAR(2) DEFAULT NULL COMMENT "포지션",
    i_1 INT(8) DEFAULT NULL COMMENT "1이닝",
    i_2  INT(8) DEFAULT NULL COMMENT "2이닝",
    i_3  INT(8) DEFAULT NULL COMMENT "3이닝",
    i_4  INT(8) DEFAULT NULL COMMENT "4이닝",
    i_5  INT(8) DEFAULT NULL COMMENT "5이닝",
    i_6  INT(8) DEFAULT NULL COMMENT "6이닝",
    i_7  INT(8) DEFAULT NULL COMMENT "7이닝",
    i_8  INT(8) DEFAULT NULL COMMENT "8이닝",
    i_9  INT(8) DEFAULT NULL COMMENT "9이닝",
    i_10  INT(8) DEFAULT NULL COMMENT "10이닝",
    i_11  INT(8) DEFAULT NULL COMMENT "11이닝",
    i_12  INT(8) DEFAULT NULL COMMENT "12이닝",
    i_13  INT(8) DEFAULT NULL COMMENT "13이닝",
    i_14  INT(8) DEFAULT NULL COMMENT "14이닝",
    i_15  INT(8) DEFAULT NULL COMMENT "15이닝",
    i_16  INT(8) DEFAULT NULL COMMENT "16이닝",
    i_17  INT(8) DEFAULT NULL COMMENT "17이닝",
    i_18  INT(8) DEFAULT NULL COMMENT "18이닝",
    hit  INT(2) DEFAULT NULL COMMENT "안타수(H)",
    bat_num  INT(2) DEFAULT NULL COMMENT "타수(AB)",
    hit_prob  DECIMAL(6,3) DEFAULT NULL COMMENT "타율(AVG)",
    hit_get  INT(2) DEFAULT NULL COMMENT "타점(RBI)",
    own_get  INT(2) DEFAULT NULL COMMENT "득점(R)",
    CONSTRAINT scoreboards_batter_idx_fk FOREIGN KEY (idx) REFERENCES scoreboard (idx),
    CONSTRAINT player_id_batter_playerid_fk FOREIGN KEY (playerid) REFERENCES player_id (playerid)
);
```

아래의 코드 입력하면 코멘트 확인 가능

```sql
show full columns from batter;
```

### Info

- idx: scoreboards의 외래키, 경기정보와 연결되어 있다.
- playerid: PlayerID의 외래키, 선수의 이름과 연결되어 있다.
- position: 특정 경기에서 해당 선수가 맡은 역할을 코드로 바꾸어 저장한다. 코드로 바꾸는 이유는 한자를 대체하기 위해서이다. 
- i_1-i_18: 특정 선수가 해당 이닝(예: i_1(1이닝))에서 수행한 타격 기록을 저장합니다. 타격 기록은 각 기록에 해당하는 4자리 숫자 코드로 변경되어 저장됩니다. 예를 들면 안타는 1루 방향 안타는 1001번과 같은 코드로 저장됩니다. 참고로 한 이닝에 두 타석이 발생하는 경우 연속된 4숫자 코드로 총 8자리 코드로 저장됩니다. 예를 들면 1루 방향 안타와 1루와 2루 사이의 안타를 기록했다면, 10001002와 같이 기록됩니다.
- hit: 선수의 안타 수를 의미합니다. 약자는 H를 사용합니다.
- bat_num: 해당 경기에서 선수가 얻은 타수를 의미합니다. 본래 At bat 으로 나타내며 약자는 AB를 사용합니다
- hit_prob: 선수의 타율을 의미합니다. 본래 Batting Average으로 나타내며 약자는 AVG를 사용합니다.
- hit_get: 해당 경기에서 선수가 얻은 타점을 의미합니다. 본래 Run Batted In으로 나타내며 약자는 RBI를 사용합니다.
- own_get: 해당 경기에서 선수가 얻은 득점을 의미합니다. 본래 Run scored로 나타내며 약자는 R을 사용합니다.

## playerid

각 선수들의 아이디와 이름을 매칭하는 테이블, 개명하는 선수들이 존재하기에 이름을 하나의 테이블로 관리한다.
