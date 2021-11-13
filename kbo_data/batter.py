""" 타자 정리 모듈

   수집한 자료에서 타자 자료만을 뽑아서 정리하기 위한 모듈

   - `get_game_info()` : `modify(data)`가 사용하는 함수
   - `modify()`: 수집한 여러개의 경기가 들어 있는 자료에서 스코어보드만 정리하는 함수
   - `output()`: 수집한 여러개의 경기가 들어 있는 자료에서 스코어보드만 뽑아 정리해 사용하기 쉽게 만드는 함수
   - `output_to_pd()`: 수집한 여러개의 경기가 들어 있는 자료에서 스코어보드만 뽑아 정리해 pandas로 변환하는 함수
   - `output_to_raw_list()`: 스코어보드만 뽑아 정리해 `dict`가 들어 있는 `list`로 반환하는 함수
   - `output_to_csv()`: 수집한 게임 자료에서 스코어보드만 뽑아 정리한 자료를 `csv` 형식 파일을 생성하는 함수
   - `output_to_tuples()`: 수집한 게임 자료에서 스코어보드만 뽑아 정리한 자료를 DB에 입력하기 위해 `tuple`로 형식으로 정리하는 함수

"""

import ast

import pandas as pd

from modifying import get_game_info


def modify(data):
    """수집한 여러 개의 경기가 들어 있는 자료에서 타자 자료만 정리하는 함수

    이 함수는 여러 경기자료(`data`)에서 스코어보드만 뽑아서 내용을 고치고 변경한 다음
    다시 원 자료(`data`)에 끼워 넣는다. 즉 반환 값에는 모든 수집한 내용이 들어 있다.
    참고로 아래 긴 `for`문은 18회까지 연장하기 위한 방법이다. 기본적으로 현재 정규 이닝은
    13회까지밖에 없지만, 예전 정규 KBO 리그에서 18회까지 있는 경우가 있어 이를 반영했다.

    Examples:

    ```python
    import json
    import batter
    with open("../sample_data/2017/2017_03.json", 'r') as json_file:
        kbo_2017_03 = json.load(json_file)
    batter_data = batter.modify(kbo_2017_03)
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
        data (json): scoreboard만 수정한, 하나 이상의 경기 자료
    """
    i = 0

    for temp in data:
        batter = [temp["contents"]["away_batter"], temp["contents"]["home_batter"]]
        for home_or_away in batter:
            for item in home_or_away:
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
            temp_batter = pd.DataFrame(home_or_away)
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
            print(ast.literal_eval(home_or_away))
            print(data[i]["contents"][home_or_away])
            data[i]["contents"][home_or_away] = ast.literal_eval(
                temp_batter.to_json(orient="records")
            )
    i = i + 1
    return data
