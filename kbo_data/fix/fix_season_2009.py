""" 2009년 시즌 자료를 수정 보완하는 라이브러리

본 파일에는 이미 추가하고자 하는 자료를 상수 형식으로 저장하고 있다.
이것을 가지고 `fix`에 들어 있는 코드를 가지고 이미 수집한 자료를 수정하고 보완한다.
다음을 수정한다.

- `fix_team_names()`을 이용하여 팀 이름이 잘못되어 있는 것을 고친다.
- 4월 4일 서울(현 키움)과 롯데 경기(20090404,WOLT0)에 타자 자료가 없는 것을 추가한다.

"""

import ast
import json
import configparser

import fix

config = configparser.ConfigParser()
config.read("kbo_data.ini", encoding="utf-8")
kbo_data_seasons = config["seasons"]
kbo_data_seasons_list = [item for item in kbo_data_seasons]

# 아래 자료는 200년 자료에 빠져 있다고 생각한 "20090404,WOLT0" 투수 자료
# 자료를 저장할 때 아래와 같이 한 줄을 내리고 자료를 csv 형식으로 저장해야 한다.
# 이렇게 저장하는 이유는 우선 저장하기 편하고, 가독성이 높기 때문이다.
# 이렇게 저장하지 않으면 코드가 제대로 작동하지 않는다.
# 물론 이 패키지를 사용하는 사람은 이것을 고칠 필요도 없고 작성할 필요도 없을 것이다.
# 아쉽게도 우리가 수집한 자료에 이미 이 투수 자료가 다 있었다.
# 나중을 위해서 자료를 남겨둔다.

home_pitchers = """
투수명,이닝,피안타,실점,자책,4사구,삼진,피홈런,타자,타수,투구수,경기,승리,패전,세이브,평균자책
송승준,6,9,2,2,3,3,0,29,26,94,1,0,0,0,3.00
김이슬,0 ⅓,0,0,0,0,0,0,1,1,6,1,0,0,0,0.00
이정민,0 ⅔,0,0,0,0,0,0,1,1,1,1,1,0,0,0.00
강영식,1,0,0,0,0,2,0,3,3,10,1,0,0,0,0.00
애킨스,1,0,0,0,0,0,0,3,3,13,1,0,0,1,0.00
"""

home_pitchers_patch = {
    "송승준": {"등판": "선발"},
    "이정민": {"결과": "승"},
    "강영식": {"결과": "홀드"},
    "애킨스": {"결과": "세"},
    "팀": "롯데",
}

# "20090404,WOLT0" 타자 자료 시작
home_batters_20090404_WOLT0 = """
타자명,포지션,타수,득점,안타,타점,홈런,볼넷,삼진,타율,1,2,3,4,5,6,7,8,9
김주찬,1루수,4,1,3,1,0,0,0,0.750,투안,유땅,,,중안,,좌2,,
이인구,중견수,2,0,0,0,0,0,0,0.000,포희번,,좌비,,3비,,,,
전준우,대타,1,0,0,0,0,0,0,0.000,,,,,,,3땅,,
최만호,대타,0,0,0,0,0,0,0,0.000,,,,,,,,,
조성환,2루수,4,0,1,1,0,0,1,0.250,중2,,유땅,,,우비,,삼진,
이대호,3루수,3,0,0,0,0,1,0,0.000,3땅,,3땅,,,3땅,,4구,
김민성,대타,0,0,0,0,0,0,0,0.000,,,,,,,,,
가르시아 우익수,4,0,0,0,0,0,1,0.000,삼진,,,2땅,,중비,,유병,
홍성흔,지명타자,3,0,0,0,0,0,0,0.000,,3땅,,좌비,,,중비,,
강민호,포수,3,1,1,1,1,0,1,0.333,,3땅,,삼진,,,좌홈,,
손아섭,좌익수,2,0,1,0,0,1,0,0.500,,4구,,,유땅,,중안,,
이승화,대타,0,1,0,0,0,0,0,0.000,,,,,,,,,
박기혁,유격수,3,0,1,0,0,0,0,0.333,,우중안,,,중비,,투땅,,
"""

home_batters_patch_20090404_WOLT0 = {
    "id": "20090404_WOLT0",
    "fixed_file_name": "2009_04.json",
    "팀": "롯데",
    "home_or_away": "home_batter",
}

away_batters_20090404_WOLT0 = """
타자명,포지션,타수,득점,안타,타점,홈런,볼넷,삼진,타율,1,2,3,4,5,6,7,8,9
이택근,중견·1루,3,0,1,0,0,2,1,0.333,중안,,4구,,삼진,,4구,,중비
강정호,유격수, 3,0,1,1,0,1,0,0.333,중비,,1땅,,중안,,4구,,
클락,좌익·중견,4,0,1,1,0,0,0,0.250,유병,,투유병,,좌안,,우비,,
브룸바,우익수,4,0,0,0,0,0,1,0.000,,삼진,,1파,중비,,2직,,
이숭용,1루수,1,0,1,0,0,0,0,1.000,,우안,,,,,,,
송지만,대타,2,0,0,0,0,0,0,0.000,,,,3땅,,투땅,,,
전준호,대타,0,0,0,0,0,0,0,0.000,,,,,,,,,
김민우,대타,1,0,0,0,0,0,1,0.000,,,,,,,,삼진,
정수성,대타,0,0,0,0,0,0,0,0.000,,,,,,,,,
오재일,지명타자,4,0,0,0,0,0,0,0.000,,좌비,,중비,,1땅,,1땅,
강귀태,포수,4,0,3,0,0,0,1,0.750,,우안,,,좌안,중안,,삼진,
김일경,2루수,3,1,1,0,0,0,1,0.333,,삼진,,,우안,유실,,,
강병식,대타,1,0,0,0,0,0,0,0.000,,,,,,,,,2땅
황재균,4,1,1,0,0,0,0,0.250,,,좌중2,,투땅,유땅,,,중비
"""

away_batters_patch_20090404_WOLT0 = {
    "id": "20090404_WOLT0",
    "fixed_file_name": "2009_04.json",
    "팀": "서울",
    "home_or_away": "away_batter",
}
# "20090404,WOLT0" 타자 자료 끝

total_fix_list = [
    (away_batters_20090404_WOLT0, away_batters_patch_20090404_WOLT0),
    (home_batters_20090404_WOLT0, home_batters_patch_20090404_WOLT0),
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
            #print(temp)
            temp_file_location = location + "/2009/" + item[1]["fixed_file_name"]
            # print(temp_file_location)
            with open(temp_file_location, "r") as json_file:
                games = json.load(json_file)

                for game in games:
                    if game["id"] == game_id:
                        game["contents"][is_home_or_away] = temp[is_home_or_away]

                with open(temp_file_location, "w") as outfile:
                    json.dump(games, outfile, ensure_ascii=False)
                    print("파일 내용 변경!")


def changing_team_names(location):
    """2009년 시즌 자료에 팀 이름이 잘못되어 있는 것을 수정하는 함수

    수집한 2009년 자료에는 히어로즈 구단 명이 없는데 이를 "서울"로 넣어야 한다.
    참고로 아래 리스트는 같은 팀이라고 할 수 있다.

    - 우리 히어로즈 (2008년)
    - 서울 히어로즈 (2008년~2009년)
    - 넥센 히어로즈 (2010년~2018년)

    이 문제에 대한 자세한 내용을 아래 링크를 참고한다.
    참고로 2008년 자료에는 "우리", 2010년 이후에는 "넥센"이라고 되어 있다.

    https://ko.wikipedia.org/wiki/키움_히어로즈

    Args:
        data (str): 수집한 하나 이상의 경기 자료

    Returns:
        data (json): 타자 자료만 수정한 하나 이상의 경기 자료
    """

    for item in ast.literal_eval(kbo_data_seasons["2009"]):
        temp_file_location = location + "/2009/" + "2009_" + item + ".json"
        with open(temp_file_location, "r") as json_file:
            games = json.load(json_file)
            for game in games:
                for team_scoreboard in game["contents"]["scoreboard"]:
                    if team_scoreboard["팀"] == "":
                        team_scoreboard["팀"] = "서울"
                        #print("스코어 보드에 팀명이 없습니다. '서울'로 입력")
                for away_batter in game["contents"]["away_batter"]:
                    if away_batter["팀"] == "":
                        away_batter["팀"] = "서울"
                        #print("원정팀 타자 자료에 팀명이 없습니다. '서울'로 입력")
                for away_batter in game["contents"]["home_batter"]:
                    if away_batter["팀"] == "":
                        away_batter["팀"] = "서울"
                        #print("홈팀 타자 자료에 팀명이 없습니다. '서울'로 입력")
                for away_batter in game["contents"]["away_pitcher"]:
                    if away_batter["팀"] == "":
                        away_batter["팀"] = "서울"
                        #print("원정팀 투수 자료에 팀명이 없습니다. '서울'로 입력")
                for away_batter in game["contents"]["home_pitcher"]:
                    if away_batter["팀"] == "":
                        away_batter["팀"] = "서울"
                        #print("원정팀 투수 자료에 팀명이 없습니다. '서울'로 입력")
        with open(temp_file_location, "w") as outfile:
            json.dump(games, outfile, ensure_ascii=False)


def pitchers_data():
    """2009년 경기 중 투수 자료를 추가하는 함수

    20090404,WOLT0 경기 투수 자료를 추가하는 함수다.
    이 함수는 상위 `fix`에서 구현한 함수를 가져와 사용한다.
    본 파일에는 이미 추가하고자 하는 자료를 상수 형식으로 저장하고 있다.
    이를 이용해서 우리가 수집한 자료에서 빠진 투수 자료를 추가하게 된다.
    한 팀의 투수 자료는 아래와 같이 2개의 파일로 구성되어 있다.
    그래서 1경기 자료를 추가하려면 각각 2개씩 필요하다.

    - home_pitchers: 이건 `csv` 형식으로 자료를 저장하고 있는 것 같지만, 실제로는 `str` 형식이다.
    - home_pitchers_patch: 순수하게 `dict`로 저장한다.

    아쉽게도 20090404,WOLT0 경기를 가지고 코드를 작성했지만,
    이 프로젝트 코드를 가지고 수집한 자료에는 이미 투수 자료가 다 있었다.
    타자 자료가 없는 것이었다. 그래서 이 함수는 다른 투수 자료가 빠진 곳에서
    사용할 때 참고하기하기 위에 여기에 남겨둔다.

    Returns:
        temp_dict (json): 투수 자료
    """

    temp = fix.changing_naver_pitchers_col_name(home_pitchers)
    temp = fix.changing_str_to_list_in_csv(temp)
    temp = fix.changing_naver_pitchers_list_to_dict(temp, home_pitchers_patch)
    temp = fix.changing_naver_pitchers_inning_format(temp)
    temp_dict = {}
    temp_dict["home_pitcher"] = temp
    print(temp_dict)
