# 스코어보드

각 게임의 스코어보드를 저장하는 스키마

## schema

```python
idx = Column(Integer)
team = Cloumn(String)
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
i_13 = Column(Integer)
i_14 = Column(Integer)
i_15 = Column(Integer)
i_16 = Column(Integer)
i_17 = Column(Integer)
i_18 = Column(Integer)
r = Column(Integer)
h = Column(Integer)
e = Column(Integer)
b = Column(Integer)
year = Column(Integer)
month = Column(Integer)
day = Column(Integer)
week = Column(Integer)
home = Column(String)
away = Column(String)
dbheader = Column(Integer)
```

## primary key
기본키는 년도(4글자)+월일(4글자)+더블헤더유무(1글자)+팀번호(2글자)로 조합된 복합 인조식별자입니다.

- 더블헤더
```
0: 더블헤더경기 아님
1: 더블헤더 경기(1번)
2: 더블헤더 경기(2번)
```

- 팀 번호
```
[TEAM]
두산: 1
롯데: 2
삼성: 3
한화: 4
LG: 5
KIA: 6
SK: 7
현대: 8
우리: 8
넥센: 8
키움: 8
NC: 9
KT: 10
SSG: 11
```

## 각 컬럼 설명

- idx: 해당 경기의 값들을 조합하여 만든 primary key. 선수들 table과 연결
- team: 팀명 (3글자)
- result: 해당 팀 승리는 `int 1`, 패배는 `int -1`, 무승부는 `int 1` 로 저장
- i_1 ~ i_8 (Integer) : 점수 저장
- i_9 ~ i_18 (Integer) : 값이 `-1`이 들어있을 수도 있다. 이런 경우는 해당 이닝 경기가 발생하지 않은 경우이다. `null`값으로 하지 않은 이유는 나중에 해당 열을 `(Integer)`로 변환하기 쉽게 하기 위해서이다.
- r: 해당 팀이 경기에서 얻은 총 득점의 수를 나타냅니다.
- h: 해당 팀이 경기에서 얻은 총 안타의 수를 나타냅니다.
- e: 해당 팀이 경기에서 발생한 총 실책의 수를 나타냅니다.
- b: 해당 팀이 경기에서 발생한 총 사사구(볼넷과 데드볼의 합)의 수를 나타냅니다.
- year: 해당 경기가 진행한 날짜 중 년도를 나타냅니다.
- month: 해당 경기가 진행한 날짜 중 월을 나타냅니다.
- day: 해당 경기가 진행한 날짜 중 일을 나타냅니다.
- week: 해당 경기가 진행한 날의 요일을 나타냅니다. 1~6까지의 값이 있습니다. 1은 화요일, 2는 수요일 3은 목요일 ... 6은 일요일 입니다. 월요일은 경기가 진행되지 않기에 0번이 빠집니다.
- home ~ away: 해당 경기의 홈팀과 원정팀이 어떤 팀인지를 나타냅니다.
- dbheader: 더불헤더가 아닌 날짜의 경기는 0, 더블헤더 경기 중 첫 번째 경기는 1, 두 번째 경기는 2를 나타냅니다.

## SQLite로 kbo DB를 만들어 테스트 하기

SQLite로 `kbo.db`이라는 파일을 만들어서 DB를 구축한 다음, KBO 자료를 입력해 보겠습니다. 아래 코드에서 `sa.create_engine("sqlite:///kbo.db")`을 실행하면 현재 폴더에 `kbo.db` 파일이 만들어 DB를 구축합니다.

```python
import sqlalchemy as sa

conn = sa.create_engine("sqlite:///kbo.db")
meta = sa.MetaData()

scoreboard = sa.Table(
    "scoreboard",
    meta,
    sa.Column("idx", sa.Integer, primary_key=True),
    sa.Column("team", sa.String),
    sa.Column("result", sa.Integer),
    sa.Column("i_1", sa.Integer),
    sa.Column("i_2", sa.Integer),
    sa.Column("i_3", sa.Integer),
    sa.Column("i_4", sa.Integer),
    sa.Column("i_5", sa.Integer),
    sa.Column("i_6", sa.Integer),
    sa.Column("i_7", sa.Integer),
    sa.Column("i_8", sa.Integer),
    sa.Column("i_9", sa.Integer),
    sa.Column("i_10", sa.Integer),
    sa.Column("i_11", sa.Integer),
    sa.Column("i_12", sa.Integer),
    sa.Column("i_13", sa.Integer),
    sa.Column("i_14", sa.Integer),
    sa.Column("i_15", sa.Integer),
    sa.Column("i_16", sa.Integer),
    sa.Column("i_17", sa.Integer),
    sa.Column("i_18", sa.Integer),
    sa.Column("r", sa.Integer),
    sa.Column("h", sa.Integer),
    sa.Column("e", sa.Integer),
    sa.Column("b", sa.Integer),
    sa.Column("year", sa.Integer),
    sa.Column("month", sa.Integer),
    sa.Column("day", sa.Integer),
    sa.Column("week", sa.Integer),
    sa.Column("home", sa.String),
    sa.Column("away", sa.String),
    sa.Column("dbheader", sa.Integer),
)

meta.create_all(conn)


import utility
temp_data = utility.get_one_day_game_data()
import scoreboards
temp = scoreboards.output_to_tuples(temp_data)

for item in temp:
    conn.execute(scoreboard.insert(item))
```

앞에서 입력한 확인합니다.

```python
result = conn.execute(scoreboard.select())
rows = result.fetchall()
print(rows)
```

결과는 다음과 같이 나올 것입니다.

```python
>>> print(rows)
[(20210408001, '두산', -1, 0, 0, 0, 0, 0, 0, 1, 0, 0, None, None, None, None, None, None, None, None, None, 1, 5, 1, 4, 2021, 4, 8, 3, '두산', '삼성', 0), (20210408002, '롯데', 1, 1, 1, 2, 0, 0, 1, 1, 0, 2, None, None, None, None, None, None, None, None, None, 8, 13, 1, 10, 2021, 4, 8, 3, 'NC', '롯데', 0), (20210408003, '삼성', 1, 1, 0, 1, 1, 0, 3, 0, 0, 0, None, None, None, None, None, None, None, None, None, 6, 9, 0, 4, 2021, 4, 8, 3, '두산', '삼성', 0), (20210408004, '한화', -1, 0, 0, 0, 4, 0, 0, 0, 0, 0, None, None, None, None, None, None, None, None, None, 4, 4, 1, 6, 2021, 4, 8, 3, 'SSG', '한화', 0), (20210408005, 'LG', 1, 0, 0, 0, 0, 6, 0, 0, 1, 0, None, None, None, None, None, None, None, None, None, 7, 10, 1, 4, 2021, 4, 8, 3, 'KT', 'LG', 0), (20210408006, 'KIA', 1, 0, 0, 0, 1, 0, 0, 0, 0, 4, None, None, None, None, None, None, None, None, None, 5, 7, 0, 7, 2021, 4, 8, 3, '키움', 'KIA', 0), (20210408008, '키움', -1, 0, 0, 0, 0, 0, 2, 1, 0, 0, None, None, None, None, None, None, None, None, None, 3, 4, 0, 8, 2021, 4, 8, 3, '키움', 'KIA', 0), (20210408009, 'NC', -1, 0, 0, 3, 0, 1, 0, 0, 0, 0, None, None, None, None, None, None, None, None, None, 4, 6, 1, 12, 2021, 4, 8, 3, 'NC', '롯데', 0), (20210408010, 'KT', -1, 0, 0, 0, 0, 1, 0, 0, 0, 2, None, None, None, None, None, None, None, None, None, 3, 8, 1, 5, 2021, 4, 8, 3, 'KT', 'LG', 0), (20210408011, 'SSG', 1, 1, 0, 2, 1, 0, 0, 0, 2, None, None, None, None, None, None, None, None, None, None, 6, 8, 2, 5, 2021, 4, 8, 3, 'SSG', '한화', 0)]
```

SQLite를 실행해서 앞에서 만든 `kbo.db`에 들어 있는 `scoreboard` 테이블을 확인해 봅니다. SQLite에서는 `Bool` 자료형이 없기 때문에 `Integer`형으로 변환되어서 입력되었습니다. 빈칸은 `None`이 SQLite에서 `NULL`로 입력된 것입니다.

```bash
❯ sqlite3 kbo.db
SQLite version 3.32.3 2020-06-18 14:16:19
Enter ".help" for usage hints.
sqlite> .tables
scoreboard
sqlite> select * from scoreboard;
20210408001|두산|-1|0|0|0|0|0|0|1|0|0||||||||||1|5|1|4|2021|4|8|3|두산|삼성|0
20210408002|롯데|1|1|1|2|0|0|1|1|0|2||||||||||8|13|1|10|2021|4|8|3|NC|롯데|0
20210408003|삼성|1|1|0|1|1|0|3|0|0|0||||||||||6|9|0|4|2021|4|8|3|두산|삼성|0
20210408004|한화|-1|0|0|0|4|0|0|0|0|0||||||||||4|4|1|6|2021|4|8|3|SSG|한화|0
20210408005|LG|1|0|0|0|0|6|0|0|1|0||||||||||7|10|1|4|2021|4|8|3|KT|LG|0
20210408006|KIA|1|0|0|0|1|0|0|0|0|4||||||||||5|7|0|7|2021|4|8|3|키움|KIA|0
20210408008|키움|-1|0|0|0|0|0|2|1|0|0||||||||||3|4|0|8|2021|4|8|3|키움|KIA|0
20210408009|NC|-1|0|0|3|0|1|0|0|0|0||||||||||4|6|1|12|2021|4|8|3|NC|롯데|0
20210408010|KT|-1|0|0|0|0|1|0|0|0|2||||||||||3|8|1|5|2021|4|8|3|KT|LG|0
20210408011|SSG|1|1|0|2|1|0|0|0|2|||||||||||6|8|2|5|2021|4|8|3|SSG|한화|0
```
