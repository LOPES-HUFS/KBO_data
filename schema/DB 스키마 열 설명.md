# DB 스키마 열 설명

## Tables

### PlayerID

PlayerID는 동명이인 선수를 구분하는데 필수적인 열입니다.

PlayerID = Column(Integer)
name = Column(String(20))

### TeamID

TeamID = Column(Integer)
name = Column(String(5))

### Batters

PlayerID는 해당 선수의 고유 번호입니다. position은 선수가 해당 경기에서 맡았던 역할입니다. TeamID는 해당 선수의 소속 팀에 대한 고유 값입니다. PlayerID, TeamID는 연관 테이블을 통해 고유번호에 해당하는 이름과 같은 정보를 알수 있습니다. i_1~i_12 열은 이닝 정보를 나타내는 열입니다. 일반적으로는 9회까지 진행하지만 연장경기의 가능성이 있기 때문에 12회를 의미하는 i_12 열까지 만들어 주어야 합니다.

hit 열은 안타를 의미하는 열로 약자로 H를 사용한다. bat_num은 타수로 정식 용어는 At bat으로 약자는 AB를 사용합니다. hit_prob은 평균 타율로 약자로는 AVG입니다. hit_get은 타점으로 Run Batted In 으로 약자는 RBI 입니다. own_get 득점을 의미하는 열로 Run scored 이며 약자로는 R을 사용합니다.

PlayerID = Column(Integer)
position = Column(String(3))  
TeamID = Column(Integer)
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

### Pitchers

PlayerID는 해당 선수의 고유 번호입니다. position은 선수가 해당 경기에서 맡았던 역할입니다. TeamID는 해당 선수의 소속 팀에 대한 고유 값입니다. PlayerID, TeamID는 연관 테이블을 통해 고유번호에 해당하는 이름과 같은 정보를 알수 있습니다. join 열은 등판한 회수를 말합니다. inning,rest 는 모두 던진 이닝 수를 나타내는데 이닝 열에는 최소 1회 이상이 해당되고, rest 열에 나머지 1회 미만 즉 3타자 미만 인 경우가 기록됩니다. result 열은 경기의 승리 패배 무승부를 세 가지 숫자로 기록합니다. save와 hold는 각각 세이브 기록과 홀드 기록을 보여줍니다. strikeout, deadball 삼진과 사사구에 대한 열 입니다. losescore 실점으로 약자는 타자의 득점과 같은 R을 사용합니다. earnedrun 투수의 자책점에 대한 열로 약자는 ER을 사용합니다. pitchnum 투구수로 NP를 사용합니다. hited는 피안타를 의미합니다. homerun은 피홈런을 입니다. hitnum은 타수를 의미합니다. hitter는 타자수를 의미하며 약자는 TBF를 사용합니다.

PlayerID = Column(Integer)
position = Column(String(3))
TeamID = Column(Integer)
join = Column(Integer)  
inning = Column(Integer)  
rest = Column(Integer)  
result = Column(Integer)
save = Column(Integer)
hold = Column(Integer)
strikeout = Column(Integer)
deadball = Column(Integer)
losescore = Column(Integer)
earnedrun = Column(Integer)
pitchnum = Column(Integer)
hited = Column(Integer)
homerun = Column(Integer)
hitnum = Column(Integer)
hitter = Column(Integer)

### Scoreboards

TeamID 경기를 진행한 팀에 대한 정보를 숫자로 나타냅니다. result는 경기결과에 대한 열입니다. i_1 ~ i_12 열은 이닝 정보를 나타내는 열입니다. 일반적으로는 9회까지 진행하지만 연장경기의 가능성이 있기 때문에 12회를 의미하는 i_12 열까지 만들어 주어야 합니다. R은 득점을 나타내고, H는 안타 수를 나타내며, E는 실책을 의미합니다. B는 사사구를 의미합니다. year, month, day 는 날짜를 나타내는 열입니다. week은 주를 의미합니다. home, away 어느 팀이 홈팀인지 원정팀인지를 구분하는 열입니다. dbheader는 db 프라이머리 키를 의미합니다.
추가로 배터 와 피쳐 테이블에 연결할 수 있는 연결 키가 필요한 열입니다.

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