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

import pandas as pd

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

    Examples:

    ```python
    import json
    import pitchers
    with open("../sample_data/2017/2017_03.json", 'r') as json_file:
        kbo_2017_03 = json.load(json_file)
    kbo_2017_03_modifed = pitchers.modify(kbo_2017_03)
    ```

    Note:
        현재 수정하거나 추가하고 있는 컬럼 이름
        - 승패
        - 홈팀
        - 원정팀
        - 더블헤더

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
            # 여기서 투수 자료에서 아래와 같은 것을 추가하고 있다.
            for pitcher in pitchers:
                pitcher["year"] = game_info["year"]
                pitcher["month"] = game_info["month"]
                pitcher["day"] = game_info["day"]
                pitcher["week"] = game_info["week"]
                pitcher["홈팀"] = single_game["contents"]["scoreboard"][1]["팀"]
                pitcher["원정팀"] = single_game["contents"]["scoreboard"][0]["팀"]
                pitcher["더블헤더"] = game_info["더블헤더"]
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
