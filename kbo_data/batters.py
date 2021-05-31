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

Batter_factor = config["BATTER"]

def change_record(temp,column):
   '''
   temp: 타자 DataFrame 파일을 의미한다.
   column: 선수의 타격 기록이 있는 이닝 열을 의미한다. 
   사용방법
   import pandas as pd
   temp = pd.read_json("20210409_KTSS0.json")
   batter = pd.DataFrame(temp['20210409_KTSS0']["away_batter"])
   change_record(batter,1)
   '''
    for i in list(Batter_factor.keys()):
        temp = temp.replace(i,Batter_factor[i])
    for i in range(0,len(temp[[str(column)]])):
        if "/" in list(str(temp[str(column)].tolist()[i])):
            temp1 = Batter_factor[str(temp[str(column)].tolist()[i].split("/ ")[0].split("\\")[0])]
            temp2 = Batter_factor[str(temp[str(column)].tolist()[i].split("/ ")[1])]
            temp.loc[i,str(column)] = str(temp1)+str(temp2)
    return temp

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
