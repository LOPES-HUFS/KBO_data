""" 2008년 시즌 자료를 수정 보완하는 라이브러리

본 파일에는 이미 추가하고자 하는 자료를 상수 형식으로 저장하고 있다.
이것을 가지고 `fix`에 들어 있는 코드를 가지고 이미 수집한 자료를 수정하고 보완한다.
다음을 수정한다.

- 4월 4일 서울(현 키움)과 롯데 경기(20080330,LTHH0)에 타자 자료가 없는 것을 추가한다.

Examples:

```python
    >>> import fix
    >>> fix.season_2009("../sample_date")
    수집한 KBO 자료가 해당 디렉토리에 없습니다.
    >>> fix.season_2009("../sample_data")
    ../sample_data/2021/2021_04.json
    ../sample_data
    patch complete!
    patch complete!
```

"""

import ast
import json
import configparser

import fix

config = configparser.ConfigParser()
config.read("kbo_data.ini", encoding="utf-8")
kbo_data_seasons = config["seasons"]
kbo_data_seasons_list = [item for item in kbo_data_seasons]


# "20080330,LTHH0" 타자 자료 시작
home_batters_20080330_LTHH0 = """
타자명,포지션,타수,득점,안타,타점,홈런,볼넷,삼진,타율,1,2,3,4,5,6,7,8,9
고동진,우익수,5,1,1,0,0,0,1,0.200,3땅,,우안,,유직,,삼진,,유땅
추승우,좌익수,4,1,2,2,0,1,1,0.375,2땅,,중2,,중안,,4구,,삼진
클락,중견수,3,1,0,0,0,1,1,0.000,투땅,,2땅,,4구,,삼진,,
김태완,1루수,4,1,1,3,1,0,1,0.429,,삼진,,유땅,좌홈,,,좌비,
이영우,지명타자,3,1,1,0,0,0,0,0.286,,중비,,중안,우비,,,,
이도형,대타,1,0,0,0,0,0,0,0.000,,,,,,,,2비,
이범호,3루수,4,2,2,3,2,0,0,0.250,,우비,,중홈,,좌비,,좌홈,
한상훈,2루수,3,0,0,0,0,0,1,0.000,,,좌비,삼진,,2땅,,,
조원우,대타,0,0,0,0,0,0,0,0.000,,,,,,,,,
송광민,대타,1,0,1,0,0,0,0,1.000,,,,,,,,유안,
김수연,대타,0,0,0,0,0,0,0,0.250,,,,,,,,,
백승룡,대타,0,0,0,0,0,0,0,0.000,,,,,,,,,
신경현,포수,2,1,0,0,0,1,0,0.200,,,4구,우비,,유비,,,
윤재국,대타,1,0,0,0,0,0,1,0.000,,,,,,,,삼진,
이희근,대타,0,0,0,0,0,0,0,0.000,,,,,,,,,
김민재,유격수,4,0,0,0,0,0,0,0.000,,,좌비,,좌비,,3비,,3땅
"""

home_batters_patch_20080330_LTHH0 = {
    "id": "20080330_LTHH0",
    "fixed_file_name": "2008_03.json",
    "팀": "한화",
    "home_or_away": "home_batter",
}

away_batters_20080330_LTHH0 = """
타자명,포지션,타수,득점,안타,타점,홈런,볼넷,삼진,타율,1,2,3,4,5,6,7,8,9
정수근,좌익수,3,2,3,0,0,0,0,0.714,중안,,중안,좌2,,,,,
이승화,대타,2,1,1,0,0,0,0,0.500,,,,,,,좌안,1땅,
김주찬,중견·좌익,5,1,3,0,0,0,0,0.444,중비,,3안,,유안,,좌안,,좌비
박현승,1루수,4,1,1,0,0,0,2,0.222,삼진,,좌안,,삼진,,유2병,,
최만호,대타,1,0,0,0,0,0,0,0.000,,,,,,,,,2파
이대호,3루수,4,2,2,5,1,0,0,0.667,중안,,좌중홈,,포파,,사구,,2땅
박남섭,대타,0,0,0,0,0,0,0,0.000,,,,,,,,,
가르시아,우익수,4,1,1,3,1,0,1,0.143,1땅,,삼진,,2땅,,좌홈,,
강민호,포수,4,0,1,0,0,0,1,0.250,,1파,삼진,,,좌안,2비,,
마해영,지명타자,3,1,1,1,1,1,0,0.333,,중비,,4구,,32병,,좌중홈,
조성환,2루수,3,0,0,0,0,1,0,0.375,,2비,,우비,,4구,,유땅,
박기혁,유격수,4,0,0,0,0,0,0,0.286,,,우비,3비,,2비,,우비,
"""

away_batters_patch_20080330_LTHH0 = {
    "id": "20080330_LTHH0",
    "fixed_file_name": "2008_03.json",
    "팀": "롯데",
    "home_or_away": "away_batter",
}
# "20080330,LTHH0" 타자 자료 끝

total_fix_list = [
    (home_batters_20080330_LTHH0, home_batters_patch_20080330_LTHH0),
    (away_batters_20080330_LTHH0, away_batters_patch_20080330_LTHH0),
]

def game_data(location):
    """게임 데이터에서 빠진 부분을 가지고 있는 자료를 가지고 채워 넣는 함수

    Args:
        location (str) : 우리가 수집한 자료 파일이 들어 있는 위치
    """

    print(location)
    for item in total_fix_list:
        is_home_or_away = item[1]["home_or_away"]
        game_id = item[1]["id"]
        if is_home_or_away == "away_batter" or is_home_or_away == "home_batter":
            temp = fix.batters_data(item[0], item[1])
            # print(temp)
            temp_file_location = location + "/2008/" + item[1]["fixed_file_name"]
            # print(temp_file_location)
            with open(temp_file_location, "r") as json_file:
                games = json.load(json_file)

                for game in games:
                    if game["id"] == game_id:
                        game["contents"][is_home_or_away] = temp[is_home_or_away]

                try:
                    with open(temp_file_location, "w") as outfile:
                        json.dump(games, outfile, ensure_ascii=False)
                        print("patch complete!")
                except Exception as e:
                    print(e)
