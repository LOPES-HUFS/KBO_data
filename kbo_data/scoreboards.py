"""스코어보드 정리 모듈

   수집한 자료에서 스코어보드만을 뽑아서 정리하기 위한 모듈입니다.

   - `modify()`: 수집한 여러개의 경기가 들어 있는 자료에서 스코어보드만 정리하는 함수
   - `output()`: 수집한 여러개의 경기가 들어 있는 자료에서 스코어보드만 뽑아 정리해 사용하기 쉽게 만드는 함수
   - `output_to_pd()`: 수집한 여러개의 경기가 들어 있는 자료에서 스코어보드만 뽑아 정리해 pandas로 변환하는 함수
   - `output_to_raw_list()`: 스코어보드만 뽑아 정리해 `dict`가 들어 있는 `list`로 반환하는 함수
   - `output_to_csv()`: 수집한 게임 자료에서 스코어보드만 뽑아 정리한 자료를 `csv` 형식 파일을 생성하는 함수
   - `output_to_tuples()`: 수집한 게임 자료에서 스코어보드만 뽑아 정리한 자료를 DB에 입력하기 위해 `tuple`로 형식으로 정리하는 함수

"""

import ast
import pandas as pd

from modifying import changing_win_or_loss_to_int
from modifying import is_exist_inning
from modifying import making_primary_key
from modifying import get_game_info

def modify(data):
    """수집한 여러개의 경기가 들어 있는 자료에서 스코어보드만 정리하는 함수
    이 함수는 여러 경기자료(`data`)에서 스코어보드만 뽑아서 내용을 고치고 변경한 다음
    다시 원 자료(`data`)에 끼워 넣는다. 즉 반환 값에는 모든 수집한 내용이 들어 있다.
    참고로 아래 긴 `for`문은 18회까지 연장하기 위한 방법이다. 기본적으로 현재 정규 이닝은
    13회까지밖에 없지만, 예전 정규 KBO 리그에서 18회까지 있는 경우가 있어 이를 반영했다.
    Examples:
    ```python
    import json
    import scoreboards
    with open("../sample_data/2017/2017_03.json", 'r') as json_file:
        kbo_2017_03 = json.load(json_file)
    data = scoreboards.modify(kbo_2017_03)
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
        fin_boards = []
        etc_info = temp["contents"]["ETC_info"]
        game_info = get_game_info(temp["id"])
        for old_info in temp["contents"]["scoreboard"]:
            new_info = {}
            new_info["idx"] = making_primary_key(
                old_info["팀"],
                game_info["year"],
                game_info["month"],
                game_info["day"],
                game_info["더블헤더"],
                )
            new_info["team"] = old_info["팀"]
            new_info["result"] = 1 if old_info["승패"] == "승" else 0 if old_info["승패"] == "무" else -1
            new_info = add_ining(new_info, old_info)
            new_info["r"] = old_info['R']
            new_info["h"] = old_info['H']
            new_info["e"] = old_info['E']
            new_info["b"] = old_info['B']
            new_info["year"] = game_info["year"]
            new_info["month"] = game_info["month"]
            new_info["day"] = game_info["day"]
            new_info["week"] = game_info["week"]
            new_info["home"]= temp["contents"]["scoreboard"][1]["팀"]
            new_info["away"] = temp["contents"]["scoreboard"][0]["팀"]
            new_info["dbheader"] = game_info["더블헤더"]
            new_info["place"] = etc_info["구장"]
            new_info["audience"] = int(etc_info["관중"].replace(',',''))
            new_info["starttime"] =  etc_info["개시"]
            new_info["endtime"] =  etc_info["종료"]
            new_info["gametime"] =  etc_info["경기시간"]
            fin_boards.append(new_info)

        fin_boards = pd.DataFrame(fin_boards)
        data[i]["contents"]["scoreboard"] = ast.literal_eval(
                fin_boards.to_json(orient="records")
        )
        i = i + 1

    return data


def output(data):
    """수집한 여러개의 경기가 들어 있는 자료에서 스코어보드만 뽑아 정리해 사용하기 쉽게 만드는 함수

    여러 경기 자료가 같이 들어가 있는 자료에서 스코어보드만 모두 뽑아서 위 `modify` 함수를
    이용하여 처리한다. 따라서 반환하는 값에는 여러 경기의 스코어보드만 들어 있다.

    참고로 반환값이 `list` 안의 `list`로 되어 있는 이유는 한 경기가 2개의 `dict`로
    되어 있기 때문에 이 두 개를 `list`로 묶고 여러 경기를 `list`롤 다시 한 번 묶기 때문이다.
    그리고 `list`로 되어 있는 이유는 pandas를 염두에 두었기 때문이다. pandas를 통해서
    다양한 포멧으로 변환할 수 있게 만들고자 한다.

    ### Examples:

    ```python
    import json
    import scoreboards
    with open("../sample_data/2017/2017_03.json", 'r') as json_file:
        kbo_2017_03 = json.load(json_file)
    data = scoreboards.output(kbo_2017_03)
    ```

    ### Args:
        data (json): 수집된 한 게임 이상의 게임 자료

    ### Returns:
        temp_data (json): 여려 경기 스코어보드 자료
    """
    data = modify(data)

    temp_data = []

    i = 0

    for item in data:
        # print(item['contents']['scoreboard'])
        temp_p = pd.DataFrame(item["contents"]["scoreboard"])
        # print(temp_p)
        # print(ast.literal_eval(temp_p.to_json(orient='records')))
        temp_data.append(ast.literal_eval(temp_p.to_json(orient="records")))
        i = i + 1

    return temp_data


def output_to_pd(data):
    """수집한 여러개의 경기가 들어 있는 자료에서 스코어보드만 뽑아 정리해 pandas로 변환하는 함수

    여러 경기 자료가 같이 들어가 있는 자료에서 `output` 함수를 이용하여
    스코어보드만 모두 뽑고 정리해서 이렇게 처리한 자료를 pandas로 반환해 준다.
    이렇게 반환하면 아래 예에서처럼 pandas를 이용해 여러가지 분석을 할 수 있다.
    아래 활용법 참고!

    ### Examples:

    ```python
    import json
    import scoreboards
    with open("../sample_data/2017/2017_03.json", 'r') as json_file:
        kbo_2017_03 = json.load(json_file)
    data = scoreboards.output_to_pd(kbo_2017_03)
    ## 활용법
    ## 위 2017월 3월 경기 중 9회에 1점 이상 득점한 팀은?
    >>> data['team'][data.i_9 >= 1]
    0     롯데
    6    KIA
    7     삼성
    Name: team, dtype: object
    ## 위 2017월 3월 경기 중 승리한 팀은?
    >>> data['team'][data.result == "승"]
    1     NC
    3     두산
    4     KT
    6    KIA
    8     LG
    Name: team, dtype: object
    ```
    ### Args:
        data (json): 수집된 한 게임 이상의 게임 자료

    ### Returns:
        temp_data (df): 여러 경기 스코어보드 자료
    """

    data = output(data)

    temp_data = []

    for item in data:
        for sub_item in item:
            temp_data.append(sub_item)

    return pd.DataFrame(temp_data)


def output_to_raw_list(data):
    """스코어보드만 뽑아 정리해 `dict`가 들어 있는 `list`로 반환하는 함수

    여러 게임 자료를 같이 들어가 있는 자료를 `modify()`을 이용하여 스코어보드 부분만 정리한다.
    그런 다음 그 게임 자료에서 스코어보드만 뽑아서 dict로 변환한다. 다음과 같은 형식이 들어간다.

    ```json
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
        "r": 2,
        "h": 6,
        "e": 0,
        "b": 3,
        "year": 2020,
        "month": 5,
        "day": 5,
        "week": 1,
        "home": "LG",
        "away": "두산",
        "dbheader": 0,
    }
    ```

    위와 같은 것이 각 경기 당 2개가 들어가면 결국 이런 `dict`가 차례로 들어가 있는 `list`을 반환한다.

    ### Examples:

    ```python
    import json
    import scoreboards
    with open("../sample_data/2017/2017_03.json", 'r') as json_file:
        kbo_2017_03 = json.load(json_file)
    scoreboards.output_to_raw_list(kbo_2017_03)
    ```

    ### Args:
        data (dict): 수집한 한 게임 이상의 KBO 게임 자료

    ### Returns:
        temp_data (list): scoreboard를 포함하고 있는 여러 게임 자료
    """

    data = modify(data)

    # temp = [value["scoreboard"] for key, value in data.items()]
    temp = [item["contents"]["scoreboard"] for item in data]

    result = []

    for item in temp:
        result.append(item[0])
        result.append(item[1])
    return result


def output_to_csv(data, file_name="kbo_scoreboards"):
    """수집한 게임 자료에서 스코어보드만 뽑아 정리한 자료를 `csv` 형식 파일을 생성하는 함수

    앞의 `output_to_raw_list()`을 이용해서 스코어보드만 뽑아 정리한 다음
    그리고 이렇게 뽑아 정리한 자료를 csv 형식 파일을 생성한다.
    인수 `file_name`에 적절한 파일 명을 입력하면 그 파일명으로 파일을 생성한다.

    ### Examples:

    ```python
    import json
    import scoreboards
    with open("../sample_data/2017/2017_03.json", 'r') as json_file:
        kbo_2017_03 = json.load(json_file)
    scoreboards.output_to_csv(kbo_2017_03)
    ```

    앞의 Example를 실행하면 현재 폴더에 아래와 같은 내용을 가진
    `kbo_scoreboards_2020.csv`이라는 파일이 생성된다.

    ```csv
    team,result,i_1,i_2,i_3,i_4,i_5,i_6,i_7,i_8,i_9,i_10,i_11,i_12,R,H,E,B,i_13,i_14,i_15,i_16,i_17,i_18,year,month,day,week,home,away,dbheader
    롯데,패,0,0,0,1,0,0,0,3,1,-1,-1,-1,5,7,2,1,-1,-1,-1,-1,-1,-1,2017,3,31,4,NC,롯데,0
    NC,승,0,0,0,0,0,3,3,0,-1,-1,-1,-1,6,11,2,6,-1,-1,-1,-1,-1,-1,2017,3,31,4,NC,롯데,0
    한화,패,0,0,0,0,0,0,0,0,0,-1,-1,-1,0,4,4,3,-1,-1,-1,-1,-1,-1,2017,3,31,4,두산,한화,0
    두산,승,0,0,1,0,0,1,1,0,-1,-1,-1,-1,3,4,1,4,-1,-1,-1,-1,-1,-1,2017,3,31,4,두산,한화,0
    KT,승,1,1,0,1,0,0,0,0,0,-1,-1,-1,3,9,1,2,-1,-1,-1,-1,-1,-1,2017,3,31,4,SK,KT,0
    SK,패,0,0,1,0,1,0,0,0,0,-1,-1,-1,2,8,2,1,-1,-1,-1,-1,-1,-1,2017,3,31,4,SK,KT,0
    KIA,승,0,1,0,0,0,1,0,4,1,-1,-1,-1,7,7,1,8,-1,-1,-1,-1,-1,-1,2017,3,31,4,삼성,KIA,0
    삼성,패,0,0,0,1,0,0,0,0,1,-1,-1,-1,2,7,1,1,-1,-1,-1,-1,-1,-1,2017,3,31,4,삼성,KIA,0
    LG,승,0,1,1,0,0,0,0,0,0,-1,-1,-1,2,4,1,3,-1,-1,-1,-1,-1,-1,2017,3,31,4,넥센,LG,0
    넥센,패,0,0,0,0,0,1,0,0,0,-1,-1,-1,1,5,1,4,-1,-1,-1,-1,-1,-1,2017,3,31,4,넥센,LG,0
    ```

    Args:
        data (json): 수집한 한 게임 이상의 게임 자료
        file_name (str): csv로 출력할 때 확장자를 제외한 파일명

    """

    temp = output_to_raw_list(data)
    temp = pd.DataFrame(temp)
    temp_file_name = file_name + ".csv"
    return temp.to_csv(temp_file_name, index=False)


def output_to_tuples(data):
    """수집한 게임 자료에서 스코어보드만 뽑아 정리한 자료를 DB에 입력하기 위해 `tuple`로 형식으로 정리하는 함수

    앞의 `output_to_raw_list()`을 이용해서 스코어보드만 뽑아 정리한 다음
    그리고 이렇게 뽑아 정리한 자료를 각 팀 결과를 `tuple`로 바꾼 다음 이를 `list`으로 묶어서 반환한다.

    ### Examples:

    ```python
    import json
    import scoreboards
    with open("../sample_data/2017/2017_03.json", 'r') as json_file:
        kbo_2017_03 = json.load(json_file)
    scoreboards.output_to_tuples(kbo_2017_03)
    ```

    Args:
        data (json): 수집한 한 게임 이상의 게임 자료

    Returns:
        (list): `tuple`로 바꾼 scoreboard 자료

    """

    temp = output_to_raw_list(data)

    results = []

    for item in temp:
        temp_primary_key = making_primary_key(
            item["team"], item["year"], item["month"], item["day"], item["dbheader"]
        )
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
            item["r"],
            item["h"],
            item["e"],
            item["b"],
            item["year"],
            item["month"],
            item["day"],
            item["week"],
            item["home"],
            item["away"],
            item["dbheader"],
            item["place"],
            item["audience"],
            item["starttime"],
            item["endtime"],
            item["gametime"],
        )

        results.append(temp)

    return results


def output_to_dict(data):
    """수집한 게임 자료에서 스코어보드만 뽑아 정리한 자료를 DB에 입력하기 위해 dict로 형식으로 정리하는 함수

    ### Examples:

    ```python
    import json
    import scoreboards
    with open("../sample_data/2017/2017_03.json", 'r') as json_file:
        kbo_2017_03 = json.load(json_file)
    scoreboards.output_to_dict(kbo_2017_03)
    ```

    Args:
        data (json): 수집한 한 게임 이상의 게임 자료

    Returns:
        (list): dict로 바꾼 scoreboard 자료

    """

    temp = output_to_raw_list(data)

    results = []

    for item in temp:
        temp_primary_key = making_primary_key(
            item["team"], item["year"], item["month"], item["day"], item["dbheader"]
        )

        temp = {
            "idx": int(temp_primary_key),
            "team": item["team"],
            "result": changing_win_or_loss_to_int(item["result"]),
            "i_1": item["i_1"],
            "i_2": item["i_2"],
            "i_3": item["i_3"],
            "i_4": item["i_4"],
            "i_5": item["i_5"],
            "i_6": item["i_6"],
            "i_7": item["i_7"],
            "i_8": item["i_8"],
            "i_9": is_exist_inning(item["i_9"]),
            "i_10": is_exist_inning(item["i_10"]),
            "i_11": is_exist_inning(item["i_11"]),
            "i_12": is_exist_inning(item["i_12"]),
            "i_13": is_exist_inning(item["i_13"]),
            "i_14": is_exist_inning(item["i_14"]),
            "i_15": is_exist_inning(item["i_15"]),
            "i_16": is_exist_inning(item["i_16"]),
            "i_17": is_exist_inning(item["i_17"]),
            "i_18": is_exist_inning(item["i_18"]),
            "r": item["r"],
            "h": item["h"],
            "e": item["e"],
            "b": item["b"],
            "year": item["year"],
            "month": item["month"],
            "day": item["day"],
            "week": item["week"],
            "home": item["home"],
            "away": item["away"],
            "dbheader": item["dbheader"],
            "place": item["place"],
            "audience": item["audience"],
            "starttime": item["starttime"],
            "endtime": item["endtime"],
            "gametime": item["gametime"],

        }

        results.append(temp)

    return results

def add_ining(new_data, data):
    """
    이닝 수를 최대값인 18에 맞춰서 추가해주고 키 이름도 변경해주는 함수
    """

    for i in range(1, 19):
        if str(i) in data:
            new_data["i_"+str(i)] = data[str(i)]
        else:
            # 데이터 추가
            new_data["i_" + str(i)] = "-"

    return new_data
