"""스코어보드 정리 모듈

   수집한 자료에서 스코어보드를 정리하기 위한 모듈입니다.

   - `get_game_info()` : `modify(data)`가 사용하는 함수


"""

import ast
import datetime

import pandas as pd

from modifying import changing_team_name_into_id
from modifying import changing_win_or_loss_to_int
from modifying import changing_dbheader_to_bool
from modifying import is_exist_inning


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
        "더블헤더": int(temp_team[4:]),
    }
    temp.update(temp_team)

    return temp


def making_primary_key(team_name, year, month, day, dbheader):
    """스코어보드 DB에서 사용할 Primary Key를 작성하는 함수

    Examples:

        ```python
        year = 2021
        month = 4
        day = 29
        team_name = '두산'
        dbheader = 0

        import scoreboards
        scoreboards.making_primary_key(team_name, year, month, day, dbheader)
        '20210429001'
        ```

    Args:
        year (int):
        month (int) :
        day (int) :
        team_name (str) : 팀명 EG: 두산
        dbheader (int) : 더블해더 경기 유무.  아니다: 0, 1차전: 1, 2차전: 2

    Returns:
        (str): 숫자 길이가 11인 자연수. E.G.: '20210429001'
    """
    result = (
        str(year)
        + str(month).zfill(2)
        + str(day).zfill(2)
        + str(dbheader)
        + changing_team_name_into_id(team_name).zfill(2)
    )

    return result


def modify(data):
    """수집한 게임 자료에서 스코어보드만 뽑아서 정리하는 함수

    이 함수는 여러 게임 자료(`data`)에서 스코어보드만 뽑아서 내용을 고치고 변경합니다.
    그런 다음 다시 이렇게 작업한 스코어보드를 다시 원 자료(`data`)에 끼워 넣는다.
    아래 긴 `for`문은 18회까지 연장하기 위한 방법입니다.
    기본적으로 정규 이닝은 13회까지밖에 없지만, 예전 리크에서 18회까지 있는 경우가 있어
    이를 반영했습니다. 

    Examples:

        ```python
        import utility
        temp_data = utility.get_one_day_game_data()
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
        temp = value["scoreboard"]
        for item in temp:
            if "13" in item:
                pass
            else:
                item["13"] = "-"
            if "14" in item:
                pass
            else:
                item["14"] = "-"
            if "15" in item:
                pass
            else:
                item["15"] = "-"
            if "16" in item:
                pass
            else:
                item["16"] = "-"
            if "17" in item:
                pass
            else:
                item["17"] = "-"
            if "18" in item:
                pass
            else:
                item["18"] = "-"
        temp_p = pd.DataFrame(temp)
        game_info = get_game_info(key)
        temp_p.loc[:, "year"] = game_info["year"]
        temp_p.loc[:, "month"] = game_info["month"]
        temp_p.loc[:, "day"] = game_info["day"]
        temp_p.loc[:, "week"] = game_info["week"]
        temp_p.loc[:, "홈팀"] = value["scoreboard"][1]["팀"]
        temp_p.loc[:, "원정팀"] = value["scoreboard"][0]["팀"]
        temp_p.loc[:, "더블헤더"] = game_info["더블헤더"]
        temp_p.rename(
            columns={
                "팀": "team",
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
                "13": "i_13",
                "14": "i_14",
                "15": "i_15",
                "16": "i_16",
                "17": "i_17",
                "18": "i_18",
                "홈팀": "home",
                "원정팀": "away",
                "더블헤더": "dbheader",
            },
            inplace=True,
        )
        temp_p.replace("-", -1, inplace=True)
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
            "team": "두산",
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
            "team": "키움",
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
        data (json): 수집된 한 게임 이상의 게임 자료

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


def output_to_pd(data):

    """수집한 게임 자료에서 스코어보드만 뽑아서 정리해 pandas로 변환하는 함수

    여러 게임 자료를 같이 들어가 있는 자료에서 스코어보드만 모두 뽑아서 처리한다.
    처라한 자료를 pandas로 반환한다.
    사용 사례는 다음과 같이 2020년 전체 자료를 뽑아서 이 함수를 돌리면 확인할 수 있다.
    temp_data_2020.json 파일은 다음과 같이 다운받을 수 있습니다.

    ```bash
    wget https://raw.githubusercontent.com/LOPES-HUFS/KBO_data/main/sample_data/temp_data_2020.json
    ```


    Examples:
        ```python
        import json
        file_name = "temp_data_2020.json"
        temp_data = {}
        with open(file_name) as json_file:
            temp_data = json.load(json_file)

        import scoreboards
        temp_2020 = scoreboards.output_to_pd(scoreboards.modify(temp_data))
        # csv 파일로 내보내기
        temp_2020.to_csv('out.csv', index=False)
        ```

    pandas를 이용한 방법은 다음과 같다.
    적절하게 `df`로 변환된 자료를 이용해
    입력된 2020년 자료에서 안타를 3개 미만으로 친 경기를 한 팀만 뽑아보자.

    Examples:
        ```python
        temp_2020['team'][temp_2020.H < 3]
        ```

        결과는 다음과 같다.

        ```csv
        3        SK
        71       키움
        85       SK
        137      삼성
        218      한화
        454     KIA
        464     KIA
        546      LG
        582      LG
        778     KIA
        785      KT
        827      한화
        857      한화
        908      KT
        1033     LG
        1116     KT
        1135     두산
        1194     두산
        1268     NC
        1287     한화
        1418     키움
    ```

    Args:
        data (json): 수집된 한 게임 이상의 게임 자료

    Returns:
        temp_data (df): scoreboard를 포함하고 있는 여러 게임 자료
    """

    temp_data = []

    for key, value in data.items():
        temp_p = pd.DataFrame(value["scoreboard"])
        temp_data.extend(ast.literal_eval(temp_p.to_json(orient="records")))

    return pd.DataFrame(temp_data)


def output_to_raw_list(data):

    """수집한 게임 자료에서 스코어보드만 뽑아 정리해서 dict가 들어 있는 list로 반환하는 함수

    여러 게임 자료를 같이 들어가 있는 자료를 modify()을 이용하여 스코어보드 부분만 정리합니다.
    그런 다음 그 게임 자료에서 스코어보드만 뽑아서 dict로 변환한다. 다음과 같이 변합니다.

        {
        "team": "두산",
        "result": "패",
        "i_1": 0,
        "i_2": 0,
        "i_3": 0,
        "i_4": 1,
        "i_5": 0,
        "i_6": 0,
        "i_7": 0,
        "i_8": 0,
        "i_9": "1",
        "i_10": -1,
        "i_11": -1,
        "i_12": -1,
        "R": 2,
        "H": 6,
        "E": 0,
        "B": 3,
        "year": 2020,
        "month": 5,
        "day": 5,
        "week": 1,
        "home": "LG",
        "away": "두산",
        "dbheader": 0,
    }

    각 게임 당 2개가 됩니다. 결국 이런 dict가 차례차례로 들어 있는 list을 반환합니다.
    사용 사례는 다음과 같이 2020년 전체 자료를 뽑아서 이 함수를 돌리면 확인할 수 있습니다.
    temp_data_2020.json 파일은 다음과 같이 다운받을 수 있습니다.

    ```bash
    wget https://raw.githubusercontent.com/LOPES-HUFS/KBO_data/main/sample_data/temp_data_2020.json
    ```

    앞에서 다운받은 파일을 이용하면, 아래 Examples를 실행하실 수 있습니다.

    Examples:
        ```python
        import json
        file_name = "temp_data_2020.json"
        temp_data = {}
        with open(file_name) as json_file:
            temp_data = json.load(json_file)

        import scoreboards
        temp_2020 = scoreboards.output_to_raw_list(temp_data)
        ```

    결과는 앞에서 보여드린 `dict` 형식의 게임 스코어 자료가 들어있는 `list`로 나올 것입니다.

    Args:
        data (dict): 수집한 한 게임 이상의 KBO 게임 자료

    Returns:
        temp_data (list): scoreboard를 포함하고 있는 여러 게임 자료
    """

    data = modify(data)

    temp = [value["scoreboard"] for key, value in data.items()]

    result = []

    for item in temp:
        result.append(item[0])
        result.append(item[1])
    return result


def output_to_csv(data, file_name="kbo_scoreboards"):
    """수집한 게임 자료에서 스코어보드만 뽑아 정리한 자료를 csv 형식 파일로 출력하는 함수

    앞의 `output_to_raw_list()`을 이용해서 스코어보드만 뽑아 정리합니다.
    그리고 이렇게 뽑아 정리한 자료를 csv 형식 파일로 출력합니다.

    사용 사례는 다음과 같이 2020년 전체 자료를 뽑아서 이 함수를 돌리면 확인할 수 있습니다.
    temp_data_2020.json 파일은 다음과 같이 다운받을 수 있습니다.

    ```bash
    wget https://raw.githubusercontent.com/LOPES-HUFS/KBO_data/main/sample_data/temp_data_2020.json
    ```

    앞에서 다운받은 파일을 이용하면, 아래 Examples를 실행하실 수 있습니다.

    Example:
        ```python
        import json
        file_name = "temp_data_2020.json"
        temp_data = {}
        with open(file_name) as json_file:
            temp_data = json.load(json_file)

        import scoreboards
        temp_file_name = "kbo_scoreboards_2020"
        scoreboards.output_to_csv(temp_data, file_name = temp_file_name)
        ```

    앞의 Example를 실행하면
    현재 폴더에 `kbo_scoreboards_2020.csv`이라는 파일이 생성됩니다.

    Args:
        data (json): 수집한 한 게임 이상의 게임 자료
        file_name (str): csv로 출력할 때 확장자를 제외한 파일명

    """

    temp = output_to_raw_list(data)
    temp = pd.DataFrame(temp)
    temp_file_name = file_name + ".csv"
    return temp.to_csv(temp_file_name, index=False)


def output_to_tuples(data):
    """수집한 게임 자료에서 스코어보드만 뽑아 정리한 자료를 DB에 입력하기 위해 tuples로 형식으로 정리하는 함수

    Examples:

        ```python
        import utility
        temp_data = utility.get_one_day_game_data()
        import scoreboards
        temp = scoreboards.output_to_tuples(temp_data)
        print(temp)
        ```

    Args:
        data (json): 수집한 한 게임 이상의 게임 자료

    Returns:
        (list): tuple로 바꾼 scoreboard 자료

    """

    temp = output_to_raw_list(data)

    results = []

    for item in temp:
        temp_primary_key = making_primary_key(
            item["team"], item["year"], item["month"], item["day"], item["dbheader"]
        )
        temp_list = [item.values()]
        temp = (
            int(temp_primary_key),
            item["team"],
            changing_win_or_loss_to_int(item["result"]),
            item["i_1"],
            item["i_2"],
            item["i_3"],
            item["i_4"],
            item["i_5"],
            item["i_6"],
            item["i_7"],
            item["i_8"],
            is_exist_inning(item["i_9"]),
            is_exist_inning(item["i_10"]),
            is_exist_inning(item["i_11"]),
            is_exist_inning(item["i_12"]),
            is_exist_inning(item["i_13"]),
            is_exist_inning(item["i_14"]),
            is_exist_inning(item["i_15"]),
            is_exist_inning(item["i_16"]),
            is_exist_inning(item["i_17"]),
            is_exist_inning(item["i_18"]),
            item["R"],
            item["H"],
            item["E"],
            item["B"],
            item["year"],
            item["month"],
            item["day"],
            item["week"],
            item["home"],
            item["away"],
            changing_dbheader_to_bool(item["dbheader"]),
        )

        results.append(temp)

    return results
