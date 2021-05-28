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
    for i in list(Batter_factor.keys()):
        temp = temp.replace(i,Batter_factor[i])
    for i in range(0,len(temp[[str(column)]])):
        if "/" in list(str(temp[str(column)].tolist()[i])):
            temp1 = Batter_factor[str(temp[str(column)].tolist()[i].split("/ ")[0].split("\\")[0])]
            temp2 = Batter_factor[str(temp[str(column)].tolist()[i].split("/ ")[1])]
            temp.loc[i,str(column)] = str(temp1)+str(temp2)
    return temp
