"""타자 자료 정리 모듈

   수집한 자료에서 타자 자료만을 뽑아서 정리하기 위한 모듈

   - `modify()`: 수집한 여러개의 경기가 들어 있는 자료에서 타자 자료만 정리하는 함수
   - `output()`: 수집한 여러개의 경기가 들어 있는 자료에서 타자 자료만 뽑아 정리해 사용하기 쉽게 만드는 함수
   - `output_to_pd()`: 수집한 여러개의 경기가 들어 있는 자료에서 타자 자료만 뽑아 정리해 pandas로 변환하는 함수
   - `output_to_raw_list()`: 타자 자료만 뽑아 정리해 `dict`가 들어 있는 `list`로 반환하는 함수
   - `output_to_csv()`: 수집한 게임 자료에서 타자 자료만 뽑아 정리한 자료를 `csv` 형식 파일을 생성하는 함수
   - `output_to_tuples()`: 수집한 게임 자료에서 타자 자료만 뽑아 정리한 자료를 DB에 입력하기 위해 `tuple`로 형식으로 정리하는 함수

    Note:

    자료를 정리할 때 필요한 타자 factor는 다음과 같이 작동한다.

    ```pytyon
    Batter_factor = config["BATTER"]
    Batter_factor["12안"]
    >>> '1000'
    int(Batter_factor["12안"])
    >>> 1000
    ```

"""
import ast
import configparser
import re

import pandas as pd

from modifying import get_game_info

config = configparser.ConfigParser()
config.read("code_list.ini", encoding="utf-8")
Batter_factor = config["BATTER"]


def modify(data):
    """수집한 여러 개의 경기가 들어 있는 자료에서 타자 자료만 정리하는 함수

    이 함수는 여러 경기자료(`data`)에서 스코어보드만 뽑아서 내용을 고치고 변경한 다음
    다시 원 자료(`data`)에 끼워 넣는다. 즉 반환 값에는 모든 수집한 내용이 들어 있다.
    참고로 아래 긴 `for`문은 18회까지 연장하기 위한 방법이다. 기본적으로 현재 정규 이닝은
    13회까지밖에 없지만, 예전 정규 KBO 리그에서 18회까지 있는 경우가 있어 이를 반영했다.

    Examples:

    ```python
    import json
    import batters
    with open("../sample_data/2017/2017_03.json", 'r') as json_file:
        kbo_2017_03 = json.load(json_file)
    kbo_2017_03_modifed = batters.modify(kbo_2017_03)
    ```

    Note:
        현재 수정하고 있는 컬럼 이름
        - 이닝 이름 12개
        - 승패
        - 홈팀
        - 원정팀
        - 더블헤더

    Args:
        data (json): 수집한 하나 이상의 경기 자료

    Returns:
        data (json): 타자 자료만 수정한 하나 이상의 경기 자료
    """
    i = 0

    for temp in data:
        batters = [temp["contents"]["away_batter"], temp["contents"]["home_batter"]]
        home_or_away_list = ["away_batter", "home_batter"]
        for batter, home_or_away in zip(batters, home_or_away_list):
            for item in batter:
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
                print(item['포지션'])
            temp_batter = pd.DataFrame(batter)
            game_info = get_game_info(temp["id"])
            temp_batter.loc[:, "year"] = game_info["year"]
            temp_batter.loc[:, "month"] = game_info["month"]
            temp_batter.loc[:, "day"] = game_info["day"]
            temp_batter.loc[:, "week"] = game_info["week"]
            temp_batter.loc[:, "홈팀"] = temp["contents"]["scoreboard"][1]["팀"]
            temp_batter.loc[:, "원정팀"] = temp["contents"]["scoreboard"][0]["팀"]
            temp_batter.loc[:, "더블헤더"] = game_info["더블헤더"]
            temp_batter.rename(
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
            temp_batter.replace("-", -1, inplace=True)
            data[i]["contents"][home_or_away] = ast.literal_eval(
                temp_batter.to_json(orient="records")
            )
    i = i + 1
    return data


def change_record(data):

    """
    data: 타자 DataFrame 파일을 의미한다.
    사용방법
    import pandas as pd
    temp = pd.read_json("20210409_KTSS0.json")
    batter = pd.DataFrame(temp['20210409_KTSS0']["away_batter"])
    change_record(batter)
    """
    for j in range(1, 19):
        for i in range(0, len(data[[str(j)]])):
            if "一" in list(str(data[str(j)].tolist()[i])):
                data.loc[i, str(j)] = re.sub("一", "1", str(data[str(j)].tolist()[i]))
            if "二" in list(str(data[str(j)].tolist()[i])):
                data.loc[i, str(j)] = re.sub("二", "2", str(data[str(j)].tolist()[i]))
            if "三" in list(str(data[str(j)].tolist()[i])):
                data.loc[i, str(j)] = re.sub("三", "3", str(data[str(j)].tolist()[i]))
            if "/" in list(str(data[str(j)].tolist()[i])):
                temp1 = Batter_factor[
                    str(data[str(j)].tolist()[i].split("/ ")[0].split("\\")[0])
                ]
                temp2 = Batter_factor[str(data[str(j)].tolist()[i].split("/ ")[1])]
                data.loc[i, str(j)] = str(temp1) + str(temp2)
    for i in list(Batter_factor.keys()):
        data = data.replace(i, Batter_factor[i])

    return data


def change_posision(data):
    """
    data = pandas DF
    사용방법
    import pandas as pd
    temp = pd.read_json("20210409_KTSS0.json")
    batter = pd.DataFrame(temp['20210409_KTSS0']["away_batter"])
    change_posision(batter)
    """
    if "一" in data:
        data = data.replace("一", "3")
    elif "二" in data:
        data = data.replace("二", "4")
    elif "三" in data:
        data = data.replace("三", "5")
    elif "투" in data:
        data = data.replace("투", "1")
    elif "포" in data:
        data = data.replace("포", "2")
    elif "유" in data:
        data = data.replace("유", "6")
    elif "좌" in data:
        data = data.replace("좌", "7")
    elif "중" in data:
        data = data.replace("중", "8")
    elif "우" in data:
        data = data.replace("우", "9")
    elif "지" in data:
        data = data.replace("지", "D")
    elif "주" in data:
        data = data.replace("주", "R")
    elif "타" in data:
        data = data.replace("타", "H")
    return data


def del_dummy(data):
    del_inx = data[data["선수명"] == "데이터가 없습니다."].index
    data = data.drop(del_inx)
    return data


def change_colname(data):
    data.columns = [
        "i_1",
        "i_10",
        "i_11",
        "i_12",
        "i_13",
        "i_14",
        "i_15",
        "i_2",
        "i_3",
        "i_4",
        "i_5",
        "i_6",
        "i_7",
        "i_8",
        "i_9",
        "own_get",
        "name",
        "hit",
        "bat_num",
        "hit_prob",
        "hit_get",
        "team",
        "position",
        "i_16",
        "i_17",
        "i_18",
    ]
    data = data[
        [
            "name",
            "team",
            "position",
            "i_1",
            "i_2",
            "i_3",
            "i_4",
            "i_5",
            "i_6",
            "i_7",
            "i_8",
            "i_9",
            "i_10",
            "i_11",
            "i_12",
            "i_13",
            "i_14",
            "i_15",
            "i_16",
            "i_17",
            "i_18",
            "hit",
            "bat_num",
            "hit_prob",
            "hit_get",
            "own_get",
        ]
    ]
    return data
