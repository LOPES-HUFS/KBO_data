import ast
import datetime

import pandas as pd

from pasing_page import looking_for_team_name


def get(date):
    pd.DataFrame(temp_data["20190320_HHNC0"]["scoreboard"])


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


def input_data(data):
    """수집한 게임 자료에서 스코어보드만 뽑아서 정리하는 함수

    이 함수는 여러 게임 자료를 같이 들어가 있는 자료에서 스코어보드만 모두 뽑아서 처리한다.
    사용 사례를 다음과 같이 하루치 자료를 뽑아서 이 함수를 돌리면 확인할 수 있다.

    ```python
    import json
    file_name = "2021_04.29_games.json"
    temp_data = {}
    with open(file_name) as json_file:
            temp_data = json.load(json_file)
    import scoreboards
    temp_scoreboards = scoreboards.input_data(temp_data)
    temp_scoreboards['20210429_OBWO0']
    ```

    다음과 같은 값을 반환한다. list로 되어 있는 이유는 아래와 같이 pandas를 염두에 두었기 때문이다.
    ```python
    [
        {'팀': '두산', '승패': '승', '1': 9, '2': 0, '3': 4, '4': 0, '5': 0, '6': 0,
            '7': 0, '8': 0, '9': 2, '10': '-', '11': '-', '12': '-',
            'R': 15, 'H': 13, 'E': 0, 'B': 14,
            'year': 2021, 'month': 4, 'day': 29, 'week': 3,
            '홈팀': '두산', '원정팀': '키움', '더블헤더': 0},
        {'팀': '키움', '승패': '패', '1': 0, '2': 1, '3': 0, '4': 1, '5': 0, '6': 1,
            '7': 0, '8': 0, '9': 1, '10': '-', '11': '-', '12': '-',
            'R': 4, 'H': 7, 'E': 0, 'B': 1,
            'year': 2021, 'month': 4, 'day': 29, 'week': 3,
            '홈팀': '두산', '원정팀': '키움', '더블헤더': 0}
    ]
    ```

    다음과 같은 사용하면 쉽게 사용할 수 있다.
    ```python
    import pandas as pd
    pd.DataFrame(temp_scoreboards['20210429_OBWO0'])

        팀 승패  1  2  3  4  5  6  7  8  9 10 11 12   R   H  E   B  year  month  day  week  홈팀 원정팀  더블헤더
    0  두산  승  9  0  4  0  0  0  0  0  2  -  -  -  15  13  0  14  2021      4   29     3  두산  키움     0
    1  키움  패  0  1  0  1  0  1  0  0  1  -  -  -   4   7  0   1  2021      4   29     3  두산  키움     0

    Args:
        data (json): pd.read_csv()함수로 읽은 다음과 같은 게임 리스트

    Returns:
        (json): 리스트에 들어 있는 전체
    """
    i = 0

    temp_data = {}

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
        # print(list(data.keys())[i])
        # print(ast.literal_eval(temp_p.to_json(orient='records')))
        temp_data[list(data.keys())[i]] = ast.literal_eval(
            temp_p.to_json(orient="records")
        )
        i = i + 1

    return temp_data
