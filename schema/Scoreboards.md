# 스코어보드

각 게임의 스코어보드를 저장하는 스키마

## schema

```python
TeamID = Column(Integer)
result = Column(Integer)
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
R = Column(Integer)
H = Column(Integer)
E = Column(Integer)
B = Column(Integer)
year = Column(Integer)
month = Column(Integer)
day = Column(Integer)
week = Column(Integer)
home = Column(Integer)
away = Column(Integer)
dbheader = Column(Integer)
```

## 각 컬럼 설명

- TeamID: 해당 팀의 이름을 대신하여 팀 정보를 나타낸다. TeamID 테이블과 연동되어 해당 테이블에서 ID 별 팀 이름을 확인할 수 있다.
- result: 팀의 승리, 패배, 무승부 정보를 기록하는 열입니다.
- i_1 ~ i_8 (Integer) : 점수 저장
- i_9 ~ i_12 (Integer) : 값이 `-1`이 들어있을 수도 있다. 이런 경우는 해당 이닝 경기가 발생하지 않은 경우이다. `null`값으로 하지 않은 이유는 나중에 해당 열을 `(Integer)`로 변환하기 쉽게 하기 위해서이다.
