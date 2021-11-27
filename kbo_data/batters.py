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
from scoreboards import making_primary_key

config = configparser.ConfigParser()
config.read("code_list.ini", encoding="utf-8")
Batter_factor = config["BATTER"]

def modify(config, data):
    """수집한 여러 개의 경기가 들어 있는 자료에서 타자 자료만 정리하는 함수

    이 함수는 여러 경기자료(`data`)에서 스코어보드만 뽑아서 내용을 고치고 변경한 다음
    다시 원 자료(`data`)에 끼워 넣는다. 즉 반환 값에는 모든 수집한 내용이 들어 있다.
    참고로 아래 긴 `for`문은 18회까지 연장하기 위한 방법이다. 기본적으로 현재 정규 이닝은
    13회까지밖에 없지만, 예전 정규 KBO 리그에서 18회까지 있는 경우가 있어 이를 반영했다.

    Examples:

    ```python
    import json
    import batters
    import configparser
    import ast
    import pandas as  pd
    
    from modifying import get_game_info
    from scoreboards import making_primary_key
    from batters import change_position
    
    config = configparser.ConfigParser()
    config.read("code_list.ini", encoding="utf-8")
    
    with open("../sample_data/2017/2017_03.json", 'r') as json_file:
        kbo_2017_03 = json.load(json_file)
    kbo_2017_03_modifed = batters.modify(config["BATTER"],kbo_2017_03)
    ```
    Args:
        data (json): 수집한 하나 이상의 경기 자료

    Returns:
        data (json): 타자 자료만 수정한 하나 이상의 경기 자료
    """
    i = 0

    for single_game in data:
        home_or_away_list = ["away_batter", "home_batter"]
        game_info = get_game_info(single_game["id"])
        for home_or_away in home_or_away_list:
            batters = single_game['contents'][home_or_away]
            # 타자 자료의 경우 필요 없는 키들이 있어서 리스트를 새로 만들어서 덮어씌우기
            fin_batters=[]
            for batter in batters:
                new_info={}
                new_info['idx'] = making_primary_key(batter["팀"], game_info["year"], game_info["month"], game_info["day"], game_info["더블헤더"])
                new_info['playerid'] = batter["선수명"] #함수 만들어야 함
                new_info['position'] = change_position(batter["포지션"])
                new_info = add_ining(config,new_info,batter)
                new_info["hit"] = batter["안타"]
                new_info["bat_num"] = batter["타수"]
                new_info["hit_prob"] = batter["타율"]
                new_info["hit_get"] = batter["타점"]
                new_info["own_get"] = batter["득점"]
                fin_batters.append(new_info)

            fin_batters= pd.DataFrame(fin_batters)
            data[i]["contents"][home_or_away] = ast.literal_eval(fin_batters.to_json(orient="records"))
        i = i + 1

    return data


def output(config, data):
    """수집한 여러개의 경기가 들어 있는 자료에서 타자 자료만 뽑아 정리해 사용하기 쉽게 만드는 함수

    여러 경기 자료가 같이 들어가 있는 자료에서 타자 자료만 모두 뽑아서 위 `modify` 함수를
    이용하여 처리한다. 따라서 반환하는 값에는 여러 경기의 타자 자료만 들어 있다.

    ### Examples:

    ```python
    import json
    import batters
    with open("../sample_data/2017/2017_03.json", 'r') as json_file:
        kbo_2017_03 = json.load(json_file)
    data = batters.output(kbo_2017_03)
    ```

    ### Args:
        data (json): 수집된 한 게임 이상의 게임 자료

    ### Returns:
        temp_data (json): 여러 경기 타자 자료
    """
    data = modify(config, data)

    temp_data = []

    for single_game in data:
        home_or_away_list = ["away_batter", "home_batter"]
        for home_or_away in home_or_away_list:
            batters = single_game['contents'][home_or_away]
            for batter in batters:
                temp_data.append(batter)

    return temp_data


def output_to_pd(config, data):
    """수집한 여러개의 경기가 들어 있는 자료에서 타자 자료만 뽑아 정리해 pandas로 변환하는 함수

    여러 경기 자료가 같이 들어가 있는 자료에서 `output`함수를 이용하여
     타자 자료만 모두 뽑고 정리해서 이렇게 처리한 자료를 pandas로 반환해 준다.
    이렇게 반환하면 아래 예에서처럼 pandas를 이용해 여러가지 분석을 할 수 있다.
    아래 활용법 참고!

    ### Examples:

    ```python
    import json
    import batters
    with open("../sample_data/2017/2017_03.json", 'r') as json_file:
        kbo_2017_03 = json.load(json_file)
    data = batters.output_to_pd(kbo_2017_03)
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

    data = output(config, data)

    return pd.DataFrame(data)


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


def change_position(data):
    """
    data = pandas DF
    사용방법
    import pandas as pd
    temp = pd.read_json("20210409_KTSS0.json")
    batter = pd.DataFrame(temp['20210409_KTSS0']["away_batter"])
    change_posision(batter)
    """
    pst = re.split("\B",data)

    for _ in pst:
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


def add_ining(config,new_data,data):
    """
    이닝 수를 최대값인 18에 맞춰서 추가해주고 키 이름도 변경해주는 함수
    """
    
    for i in range(1,19):
        if str(i) in data:
            #키 이름 변경
            new_data["i_"+str(i)] = trans_code(config, str(data.pop(str(i))))
        else:
            #데이터 추가
            new_data["i_"+str(i)] = "-"
            
    return new_data


def trans_code(config, data):
    """붙어있는 이닝 결과값들을 변환해주는 코드
    Args:
        data (sting): 한글로 기록된 타격기록
    Returns:
        data (int): "code_list.ini"로 변환된 코드
    """
    temp = [config[x] for x in re.split("\W",data) if x != '']
    
    return "".join(temp)
