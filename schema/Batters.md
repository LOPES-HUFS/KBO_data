## Batters
타자들의 정보를 담은 테이블

#### schema

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

#### 

## PlayerID
각 선수들의 아이디와 이름을 매칭하는 테이블

#### schema
```sql
playerID = Column(Integer)
name = Column(String(20))
```
