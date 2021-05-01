"""스코어보드 정리 모듈

   수집한 자료에서 스코어보드를 정리하기 위한 모듈입니다.

   - `get_game_info()` : `modify(data)`가 사용하는 함수
   - 


"""

import ast
import datetime

import pandas as pd

from pasing_page import looking_for_team_name


def get_game_info(game_list):

    temp_date = game_list.split("_")[0]
    temp_date = datetime.datetime.strptime(temp_date.split("_")[0], "%Y%m%d")
    temp = {
        "year": temp_date.year,
        "month": temp_date.month,
        "day": temp_date.day,
        "week": temp_date.weekday(),
    }
    temp_team = game_list.split("_")[1]
    temp_team = {
        "홈팀": looking_for_team_name(temp_team[0:2]),
        "원정팀": looking_for_team_name(temp_team[2:4]),
        "더블헤더": int(temp_team[4:]),
    }
    temp.update(temp_team)

    return temp


def modify(data):
    """수집한 게임 자료에서 스코어보드만 뽑아서 정리하는 함수

    이 함수는 여러 게임 자료(`data`)에서 스코어보드만 뽑아서 내용을 고치고 변경합니다.
    그런 다음 다시 이렇게 작업한 스코어보드를 다시 원 자료(`data`)에 끼워 넣는다.

    Examples:

        ```python
        import json
        file_name = "2021_04.29_games.json"
        temp_data = {}
        with open(file_name) as json_file:
                temp_data = json.load(json_file)
        import scoreboards
        temp_data_scoreboards_modified = scoreboards.modify(temp_data)
        ```

    Note:
        현재 수정하고 있는 컬럼 이름
        - 이닝 이름 12개
        - 승패
        - 홈팀
        - 원정팀
        - 더블헤더

    Args:
        data (json): 수집한 하나 이상의 게임 자료

    Returns:
        data (json): scoreboard만 수정한 하나 이상의 게임 자료
    """
    i = 0

    for key, value in data.items():
        temp_p = pd.DataFrame(value["scoreboard"])
        game_info = get_game_info(key)
        temp_p.loc[:, "year"] = game_info["year"]
        temp_p.loc[:, "month"] = game_info["month"]
        temp_p.loc[:, "day"] = game_info["day"]
        temp_p.loc[:, "week"] = game_info["week"]
        temp_p.loc[:, "홈팀"] = game_info["홈팀"]
        temp_p.loc[:, "원정팀"] = game_info["원정팀"]
        temp_p.loc[:, "더블헤더"] = game_info["더블헤더"]
        temp_p.rename(
            columns={
                "승패": "result",
                "1": "i_1",
                "2": "i_2",
                "3": "i_3",
                "4": "i_4",
                "5": "i_5",
                "6": "i_6",
                "7": "i_7",
                "8": "i_8",
                "9": "i_9",
                "10": "i_10",
                "11": "i_11",
                "12": "i_12",
                "홈팀": "home",
                "원정팀": "away",
                "더블헤더": "dbheader",
            },
            inplace=True,
        )
        data[list(data.keys())[i]]["scoreboard"] = ast.literal_eval(
            temp_p.to_json(orient="records")
        )
        i = i + 1

    return data


def output(data):
    """수집한 게임 자료에서 스코어보드만 뽑아서 정리하는 함수

    이 함수는 여러 게임 자료를 같이 들어가 있는 자료에서 스코어보드만 모두 뽑아서 처리한다.
    사용 사례를 다음과 같이 하루치 자료를 뽑아서 이 함수를 돌리면 확인할 수 있다.

    Examples:
        ```python
        import json
        file_name = "2021_04.29_games.json"
        temp_data = {}
        with open(file_name) as json_file:
                temp_data = json.load(json_file)
        import scoreboards
        temp_scoreboards = scoreboards.output(scoreboards.modify(temp_data))
        temp_scoreboards['20210429_OBWO0']
        ```

    다음과 같은 값을 반환한다. `list`로 되어 있는 이유는 아래와 같이 pandas를 염두에 두었기 때문이다.

    Examples:
        ```python
        [
        {
            "팀": "두산",
            "result": "승",
            "i_1": 9,
            "i_2": 0,
            "i_3": 4,
            "i_4": 0,
            "i_5": 0,
            "i_6": 0,
            "i_7": 0,
            "i_8": 0,
            "i_9": 2,
            "i_10": "-",
            "i_11": "-",
            "i_12": "-",
            "R": 15,
            "H": 13,
            "E": 0,
            "B": 14,
            "year": 2021,
            "month": 4,
            "day": 29,
            "week": 3,
            "home": "두산",
            "away": "키움",
            "dbheader": 0,
        },
        {
            "팀": "키움",
            "result": "패",
            "i_1": 0,
            "i_2": 1,
            "i_3": 0,
            "i_4": 1,
            "i_5": 0,
            "i_6": 1,
            "i_7": 0,
            "i_8": 0,
            "i_9": 1,
            "i_10": "-",
            "i_11": "-",
            "i_12": "-",
            "R": 4,
            "H": 7,
            "E": 0,
            "B": 1,
            "year": 2021,
            "month": 4,
            "day": 29,
            "week": 3,
            "home": "두산",
            "away": "키움",
            "dbheader": 0,
            },
        ]
        ```

    pandas를 이용한 방법은 다음과 같다. 적절하게 `df`로 변환되는 것을 볼 수 있다.

    Examples:
        ```python
        import pandas as pd
        pd.DataFrame(temp_scoreboards['20210429_OBWO0'])
        ```

    Args:
        data (json): 수집한 하나 이상의 게임 자료

    Returns:
        temp_data (json): '20210429_OBWO0'와 같은 단일 게임 key 와 scoreboard를 포함하고 있는 여러 게임 자료
    """
    temp_data = {}

    i = 0

    for key, value in data.items():
        temp_p = pd.DataFrame(value["scoreboard"])
        # print(list(data.keys())[i])
        # print(ast.literal_eval(temp_p.to_json(orient='records')))
        temp_data[list(data.keys())[i]] = ast.literal_eval(
            temp_p.to_json(orient="records")
        )
        i = i + 1

    return temp_data
