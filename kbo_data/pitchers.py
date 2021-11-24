"""투수 자료 정리 모듈

   수집한 자료에서 투수 자료만을 뽑아서 정리하기 위한 모듈

   - `modify()`: 수집한 여러개의 경기가 들어 있는 자료에서 투수 자료만 정리하는 함수
   - `output()`: 수집한 여러개의 경기가 들어 있는 자료에서 투수 자료만 뽑아 정리해 사용하기 쉽게 만드는 함수
   - `output_to_pd()`: 수집한 여러개의 경기가 들어 있는 자료에서 투수 자료만 뽑아 정리해 pandas로 변환하는 함수
   - `output_to_raw_list()`: 투수 자료만 뽑아 정리해 `dict`가 들어 있는 `list`로 반환하는 함수
   - `output_to_csv()`: 수집한 게임 자료에서 투수 자료만 뽑아 정리한 자료를 `csv` 형식 파일을 생성하는 함수
   - `output_to_tuples()`: 수집한 게임 자료에서 투수 자료만 뽑아 정리한 자료를 DB에 입력하기 위해 `tuple`로 형식으로 정리하는 함수

"""
import configparser
import ast
import pandas as pd
from scoreboards import making_primary_key
from modifying import get_game_info

config = configparser.ConfigParser()
config.read("code_list.ini", encoding="utf-8")
Batter_factor = config["BATTER"]

def modify(data):
    """수집한 여러 개의 경기가 들어 있는 자료에서 투수 자료만 정리하는 함수

    이 함수는 여러 경기자료(`data`)에서 스코어보드만 뽑아서 내용을 고치고 변경한 다음
    다시 원 자료(`data`)에 끼워 넣는다. 즉 반환 값에는 모든 수집한 내용이 들어 있다.
    참고로 아래 긴 `for`문은 18회까지 연장하기 위한 방법이다. 기본적으로 현재 정규 이닝은
    13회까지밖에 없지만, 예전 정규 KBO 리그에서 18회까지 있는 경우가 있어 이를 반영했다.

    Args:
        data (json): 수집한 하나 이상의 경기 자료

    Returns:
        data (json): 투수 자료만 수정한 하나 이상의 경기 자료
    """
    i = 0

    for single_game in data:
        home_or_away_list = ["away_pitcher", "home_pitcher"]
        game_info = get_game_info(single_game["id"])
        for home_or_away in home_or_away_list:
            pitchers = single_game['contents'][home_or_away]
            # 투수 자료의 경우 필요 없는 키들이 있어서 리스트를 새로 만들어서 덮어씌우기
            fin_pitchers=[]
            for pitcher in pitchers:
                new_info={}
                new_info['idx'] = making_primary_key(pitcher["팀"], game_info["year"], game_info["month"], game_info["day"], game_info["더블헤더"])
                new_info['playerid'] = pitcher["선수명"] #함수 만들어야 함
                new_info['mound'] = pitcher['등판']
                new_info['inning'] = '0' if len(pitcher['이닝'].split())==1 else pitcher['이닝'].split()[0]
                new_info['rest'] = pitcher['이닝'].split()[-1][0]
                new_info['saved'] = pitcher['세']
                new_info['hold'] = pitcher['세'] #어디선가 홀드값이 날라간 것 같아요..찾아올게여
                new_info['strikeout'] = pitcher['삼진']
                new_info['dead4ball'] = pitcher['4사구']
                new_info['losescore'] = pitcher['실점']
                new_info['earnedrun'] = pitcher['자책']
                new_info['pitchnum'] = pitcher['투구수']
                new_info['hitted'] = pitcher['피안타']
                new_info['homerun'] = pitcher['홈런']
                new_info['battednum'] = pitcher['타수']
                new_info['batternum'] = pitcher['타자']
                fin_pitchers.append(new_info)

            fin_pitchers= pd.DataFrame(fin_pitchers)
            data[i]["contents"][home_or_away] = ast.literal_eval(fin_pitchers.to_json(orient="records"))
    i = i + 1

    return data

def output(data):
    """수집한 여러개의 경기가 들어 있는 자료에서 투수 자료만 뽑아 정리해 사용하기 쉽게 만드는 함수

    여러 경기 자료가 같이 들어가 있는 자료에서 투수 자료만 모두 뽑아서 위 `modify` 함수를
    이용하여 처리한다. 따라서 반환하는 값에는 여러 경기의 투수 자료만 들어 있다.

    ### Examples:

    ```python
    import json
    import pitchers
    with open("../sample_data/2017/2017_03.json", 'r') as json_file:
        kbo_2017_03 = json.load(json_file)
    data = pitchers.output(kbo_2017_03)
    ```

    ### Args:
        data (json): 수집된 한 게임 이상의 게임 자료

    ### Returns:
        temp_data (json): 여려 경기 투수 자료
    """
    data = modify(data)

    temp_data = []

    for single_game in data:
        home_or_away_list = ["away_pitcher", "home_pitcher"]
        for home_or_away in home_or_away_list:
            pitchers = single_game['contents'][home_or_away]
            for pitcher in pitchers:
                temp_data.append(pitcher)

    return temp_data

def output_to_pd(data):
    """수집한 여러개의 경기가 들어 있는 자료에서 타자 자료만 뽑아 정리해 pandas로 변환하는 함수

    여러 경기 자료가 같이 들어가 있는 자료에서 `output`함수를 이용하여
     타자 자료만 모두 뽑고 정리해서 이렇게 처리한 자료를 pandas로 반환해 준다.
    이렇게 반환하면 아래 예에서처럼 pandas를 이용해 여러가지 분석을 할 수 있다.
    아래 활용법 참고!

    ### Examples:

    ```python
    import json
    import pitchers
    with open("../sample_data/2017/2017_03.json", 'r') as json_file:
        kbo_2017_03 = json.load(json_file)
    data = pitchers.output_to_pd(kbo_2017_03)
    ## 활용법
    ## 위 2017월 3월 경기 중 100개 이상 투구한 선수는?
    >>> data['선수명'][data.투구수 >= 100]
    0     레일리
    14    니퍼트
    28    페트릭
    Name: 선수명, dtype: object
    ## 위 2017월 3월 경기 등판한 선수 중 안타를 3개 이상 맞은 선수는?
    >>> data['선수명'][data.피안타 >= 3]
    0     레일리
    6     원종현
    14    니퍼트
    16     로치
    20     켈리
    25     헥터
    28    페트릭
    34     소사
    39    밴헤켄
    Name: 선수명, dtype: object
    ```
    ### Args:
        data (json): 수집된 한 게임 이상의 게임 자료

    ### Returns:
        temp_data (df): 여러 경기 스코어보드 자료
    """

    data = output(data)

    return pd.DataFrame(data)
