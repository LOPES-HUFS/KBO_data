"""타자 자료 정리 모듈

   수집한 자료에서 타자 자료를 정리하기 위한 모듈입니다.

   - `get_game_info()` : `modify(data)`가 사용하는 함수
   - 

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

import configparser
import re

config = configparser.ConfigParser()
config.read('code_list.ini')
Batter_factor = config["BATTER"]

def change_record(data):

    '''
    data: 타자 DataFrame 파일을 의미한다.
    사용방법
    import pandas as pd
    temp = pd.read_json("20210409_KTSS0.json")
    batter = pd.DataFrame(temp['20210409_KTSS0']["away_batter"])
    change_record(batter)
    '''
    for j in range(1,19):
        for i in range(0,len(data[[str(j)]])):
            if "一" in list(str(data[str(j)].tolist()[i])):
                data.loc[i,str(j)] = re.sub("一","1",str(data[str(j)].tolist()[i]))
            if "二" in list(str(data[str(j)].tolist()[i])):
                data.loc[i,str(j)] = re.sub("二","2",str(data[str(j)].tolist()[i]))
            if "三" in list(str(data[str(j)].tolist()[i])):
                data.loc[i,str(j)] = re.sub("三","3",str(data[str(j)].tolist()[i]))
            if "/" in list(str(data[str(j)].tolist()[i])):
                temp1 = Batter_factor[str(data[str(j)].tolist()[i].split("/ ")[0].split("\\")[0])]
                temp2 = Batter_factor[str(data[str(j)].tolist()[i].split("/ ")[1])]
                data.loc[i,str(j)] = str(temp1)+str(temp2)
    for i in list(Batter_factor.keys()):
        data = data.replace(i,Batter_factor[i])

    return data

def change_posision(data):
    '''
    data = pandas DF
    사용방법
    import pandas as pd
    temp = pd.read_json("20210409_KTSS0.json")
    batter = pd.DataFrame(temp['20210409_KTSS0']["away_batter"])
    change_posision(batter)
    '''
    if '一' in data:
        data = data.replace("一","3")
    elif '二' in data: 
        data = data.replace("二","4")
    elif '三' in data:
        data = data.replace("三","5")
    elif "투" in data:
        data = data.replace("투","1")
    elif "포" in data:
        data = data.replace("포","2")
    elif "유" in data:
        data = data.replace("유","6")
    elif "좌" in data:
        data = data.replace("좌","7")
    elif "중" in data:
        data = data.replace("중","8")
    elif "우" in data:
        data = data.replace("우","9")
    elif "지" in data:
        data = data.replace("지","D")
    elif "주" in data:
        data = data.replace("주","R")
    elif "타" in data:
        data = data.replace("타","H")
    return data

def del_dummy(data):
    del_inx = data[data["선수명"]=="데이터가 없습니다."].index
    data = data.drop(del_inx)
    return data

def change_colname(data):
    data.columns = ["i_1","i_10","i_11","i_12","i_13","i_14","i_15","i_2","i_3","i_4","i_5","i_6","i_7",
               "i_8","i_9","own_get","name","hit","bat_num","hit_prob","hit_get","team","position",
              "i_16","i_17","i_18"]
    data = data[["name","team","position","i_1","i_2","i_3","i_4","i_5","i_6","i_7","i_8","i_9","i_10","i_11","i_12","i_13","i_14","i_15",
    "i_16","i_17","i_18","hit","bat_num","hit_prob","hit_get","own_get"]]
    return data

