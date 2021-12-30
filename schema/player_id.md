# player_id

선수들의 정보를 담은 테이블

## schema

```sql
CREATE TABLE player_id(
    playerid INT(5) NOT NULL COMMENT "선수ID",
    team VARCHAR(4)  NOT NULL COMMENT "팀이름",
    team VARCHAR(4)  NOT NULL COMMENT "선수이름"
);
```
