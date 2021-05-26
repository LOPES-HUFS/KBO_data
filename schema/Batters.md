## Batters
타자들의 정보를 담은 테이블

### schema

```sql
idx = Column(Integer)
PlayerID = Column(Integer)
position = Column(String(3))
i_1 = Column(Integer)
i_2 = Column(Integer)
i_3 = Column(Integer)
i_4 = Column(Integer)
i_5 = Column(Integer)
i_6 = Column(Integer)
i_7 = Column(Integer)
i_8 = Column(Integer)
i_9 = Column(Integer)
i_10 = Column(Integer)
i_11 = Column(Integer)
i_12 = Column(Integer)
hit = Column(Integer)
bat_num = Column(Integer)
hit_prob = Column(Integer)
hit_get = Column(Integer)
own_get = Column(Integer)
```

### Info

- idx: scoreboards의 외래키, 경기정보와 연결되어 있다.
- PlayerID: PlayerID의 외래키, 선수의 이름과 연결되어 있다.
- position: 특정 경기에서 해당 선수가 맡은 역할
- i_1-i_12: 선수의 점수 저장
- hit: 선수의 타수
- bat_num: 
- hit_prob
- hit_get
- own_get

## PlayerID
각 선수들의 아이디와 이름을 매칭하는 테이블, 개명하는 선수들이 존재하기에 이름을 하나의 테이블로 관리한다.

### schema
```sql
playerID = Column(Integer)
name = Column(String(20))
```
