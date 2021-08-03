## Batters

타자들의 정보를 담은 테이블

### schema

```sql
idx = Column(Integer)
playerid = Column(Integer)
position = Column(String(3)
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
i_13 = Column(Integer)
i_14 = Column(Integer)
i_15 = Column(Integer)
i_16 = Column(Integer)
i_17 = Column(Integer)
i_18 = Column(Integer)
hit = Column(Integer)
bat_num = Column(Integer)
hit_prob = Column(Integer)
hit_get = Column(Integer)
own_get = Column(Integer)
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

### schema

```sql
playerid = Column(Integer)
name = Column(String(20))
```


