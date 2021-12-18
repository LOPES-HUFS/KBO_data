""" 2018년 시즌 자료를 수정 보완하는 라이브러리

본 파일에는 이미 추가하고자 하는 자료를 상수 형식으로 저장하고 있다.
이것을 가지고 `fix`에 들어 있는 코드를 가지고 이미 수집한 자료를 수정하고 보완한다.
다음을 수정한다.

- 8월 1일 넥센과 SK 경기(20180801,WOSK0)는 전체 자료가 없습니다.

아래 코드를 실행하면 수집한 2018년 1월 자료 파일인 `2018_01.json`을 읽고 
이 게임 목록 마지막 위 8월 1일 넥센과 SK 경기를 추가해 넣는다. 

Examples:

```python
    >>> import fix
    >>> location = "../sample_data"
    >>> fix.fix_season_2018.game_data(location)
    ../sample_data
    수정 전 경기 숫자: 62
    home_batter 20180801_WOSK0
    dict_keys(['home_batter'])
    away_batter 20180801_WOSK0
    dict_keys(['home_batter', 'away_batter'])
    home_batter 20180801_WOSK0
    dict_keys(['home_batter', 'away_batter'])
    away_pitcher 20150708_HTWO0
    dict_keys(['home_batter', 'away_batter', 'away_pitcher'])
    수정 후 경기 숫자: 63
    patch complete!
```

"""

import json
import configparser

import fix

config = configparser.ConfigParser()
config.read("kbo_data.ini", encoding="utf-8")
kbo_data_seasons = config["seasons"]
kbo_data_seasons_list = [item for item in kbo_data_seasons]


scoreboard_20180801_WOSK0 = {
    "scoreboard": [
        {
            "팀": "넥센",
            "승패": "승",
            "1": 0,
            "2": 0,
            "3": 1,
            "4": 1,
            "5": 0,
            "6": 1,
            "7": 0,
            "8": 0,
            "9": 5,
            "R": 8,
            "H": 12,
            "E": 2,
            "B": 6,
        },
        {
            "팀": "SK",
            "승패": "패",
            "1": 0,
            "2": 0,
            "3": 1,
            "4": 7,
            "5": 0,
            "6": 3,
            "7": 1,
            "8": 2,
            "9": "-",
            "R": 14,
            "H": 20,
            "E": 1,
            "B": 2,
        },
    ]
}

ETC_info_20180801_WOSK0 = {
    "ETC_info": {
        "홈런": ["한동민(26호27호)", "최항(5호)", "로맥(35호)", "임병욱(11호)"],
        "2루타": [
            "정진기(2회)",
            "고종욱(5회)",
            "이재원(6회)",
            "박병호(9회)",
        ],
        "실책": [
            "김성현(3회)",
            "장영석(8회)",
            "박병호(8회)",
        ],
        "도루": "노수광(4회)",
        "병살타": [
            "김하성(1회)",
            "이정후(6회)",
        ],
        "심판": ["정종수", "김정국", "김병주", "이민호"],
        "구장": "문학",
        "관중": "5,976",
        "개시": "18:30",
        "종료": "21:51",
        "경기시간": "3:21",
    }
}

home_batters_20180801_WOSK0 = """
타자명,포지션,타수,득점,안타,타점,홈런,볼넷,삼진,타율,1,2,3,4,5,6,7,8,9
노수광,좌익수,5,2,3,1,0,0,0,0.328,우비,,중비,좌안,,우안,우안,,
박희수,대타,0,0,0,0,0,0,0,0.000,,,,,,,,,
강지광,대타,1,0,0,0,0,0,0,0.000,,,,,,,,유비,
한동민,지명타자,3,3,2,4,2,0,1,0.269,삼진,,우홈,우홈,,사구,,,
김동엽,대타,2,0,1,1,0,0,0,0.265,,,,,,,중안,3땅,
로맥,1루수,4,2,3,3,1,0,0,0.333,중안,,3땅,중안,,좌중홈,,,
나주환,대타,1,0,0,0,0,0,0,0.274,,,,,,,1비,,
이재원,포수,4,1,3,0,0,0,0,0.320,유땅,,,좌안/중안,,좌2,,,
이성우,대타,1,0,0,0,0,0,1,0.198,,,,,,,삼진,,
최항,3루수,4,1,2,3,1,0,1,0.320,,좌비,,우홈/중안,,삼진,,,
윤정우,대타,0,1,0,0,0,1,0,0.321,,,,,,,,4구,
김성현,2루수,4,1,1,0,0,0,0,0.277,,1땅,,우안/좌직,,중비,,,
이대수,대타,1,1,0,0,0,0,0,0.200,,,,,,,,3실,
정진기,우익수,5,0,2,1,0,0,0,0.253,,좌중2,,중비,유땅,2땅,,1안,
김강민,중견수,5,1,1,0,0,0,1,0.299,,중비,,삼진,유비,,좌안,2땅,
박승욱,유격수,5,1,2,1,0,0,1,0.353,,,삼진,좌안,유땅,,투땅,우안,
"""

home_batters_patch_20180801_WOSK0 = {
    "id": "20180801_WOSK0",
    "fixed_file_name": "2018_08.json",
    "팀": "SK",
    "home_or_away": "home_batter",
}

home_pitchers_20180801_WOSK0 = """
투수명,이닝,피안타,실점,자책,4사구,삼진,피홈런,타자,타수,투구수,경기,승리,패전,세이브,평균자책
켈리,5,6,2,1,3,5,0,24,20,94,19,9,5,0,4.72
채병용,0,3,1,1,0,0,0,3,3,8,15,2,1,1,4.02
김태훈,1 ⅓,0,0,0,1,1,0,4,3,14,40,7,3,0,3.36
이승진,0 ⅔,0,0,0,0,2,0,2,2,9,19,0,1,0,4.88
박희수,1,0,0,0,0,1,0,3,3,11,25,1,1,0,1.46
강지광,1,3,5,5,2,2,1,8,6,28,2,0,0,0,31.50
"""

home_pitchers_patch_20180801_WOSK0 = {
    "id": "20180801_WOSK0",
    "켈리": {"결과": "승"},
    "팀": "SK",
    "home_or_away": "home_pitcher",
}

away_batters_20180801_WOSK0 = """
타자명,포지션,타수,득점,안타,타점,홈런,볼넷,삼진,타율,1,2,3,4,5,6,7,8,9
이정후,우익수,3,2,1,1,0,1,1,0.345,삼진,,중안,좌희비,,2병,,,4구
김규민,좌익수,4,0,1,0,0,1,2,0.304,중안,,2실,삼진,,4구,,,삼진
김하성,유격수,4,1,1,0,0,1,0,0.302,2병,,4구,,3파,우직,,,좌안
박병호,1루수,5,1,1,2,0,0,2,0.327,,중비,유땅,,삼진,,삼진,,좌2
고종욱,지명타자,5,0,1,1,0,0,2,0.267,,삼진,2땅,,좌중2,,삼진,,2땅
김민성,3루수,2,1,2,0,0,0,0,0.288,,우중안,,중안,,,,,
장영석,대타,2,1,0,0,0,1,1,0.223,,,,,3땅,,삼진,,4구
임병욱,중견수,4,2,3,3,1,1,1,0.287,,중안,,4구,,1안,,삼진,좌중홈
김혜성,2루수,5,0,1,0,0,0,1,0.270,,2땅,,좌비,,중안,,1땅,삼진
주효상,포수,1,0,0,0,0,1,1,0.229,,,삼진,4구,,,,,
이택근,대타,1,0,1,1,0,0,0,0.307,,,,,,좌안,,,
김재현,대타,1,0,0,0,0,0,0,0.203,,,,,,,,투땅,
"""
away_batters_patch_20180801_WOSK0 = {
    "id": "20180801_WOSK0",
    "fixed_file_name": "2018_08.json",
    "팀": "넥센",
    "home_or_away": "away_batter",
}

away_pitchers_20180801_WOSK0 = """
투수명,이닝,피안타,실점,자책,4사구,삼진,피홈런,타자,타수,투구수,경기,승리,패전,세이브,평균자책
한현희,3 ⅔,12,8,8,0,3,3,23,23,75,21,8,7,0,5.18
윤영삼,1 ⅓,0,0,0,0,0,0,4,4,12,8,1,0,1,3.21
이승호,0 ⅓,3,3,3,1,1,1,5,4,18,17,0,1,0,6.11
안우진,1 ⅔,3,1,1,0,1,0,8,8,29,12,0,3,0,8.72
하영민,1,2,2,0,1,0,0,7,6,14,6,0,1,0,5.68
"""

away_pitchers_patch_20180801_WOSK0 = {
    "id": "20180801_WOSK0",
    "한현희": {"결과": "패"},
    "팀": "넥센",
    "home_or_away": "away_pitcher",
}

total_fix_list = [
    (home_batters_20180801_WOSK0, home_batters_patch_20180801_WOSK0),
    (away_batters_20180801_WOSK0, away_batters_patch_20180801_WOSK0),
    (home_pitchers_20180801_WOSK0, home_batters_patch_20180801_WOSK0),
    (away_pitchers_20180801_WOSK0, away_pitchers_patch_20180801_WOSK0),
]


def game_data(location):
    """20150708_HTWO 게임 데이터에서 빠진 부분을 가지고 있는 타자 자료를 가지고 채워 넣는 함수

    Args:
        location (str) : 우리가 수집한 자료 파일이 들어 있는 위치
    """

    print(location)
    single_game_data = {"id": "", "contents": ""}
    game_id = "20180801_WOSK0"
    temp_file_location = location + "/2018/2018_08.json"
    # print(temp_file_location)
    with open(temp_file_location, "r") as json_file:
        games = json.load(json_file)

    print(f"수정 전 경기 숫자: {len(games)}")
    is_game_id_exist = False

    for game in games:
        if game["id"] == game_id:
            print(game["id"]["contents"])
            is_game_id_exist = True
        else:
            is_game_id_exist = False

    if is_game_id_exist == False:
        temp_game_data = fix.both_batters_and_pitchers_data(total_fix_list)
        temp_game_data.update(scoreboard_20180801_WOSK0)
        temp_game_data.update(ETC_info_20180801_WOSK0)
        single_game_data["contents"] = temp_game_data
        single_game_data["id"] = game_id
    else:
        print("오류!")

    games.append(single_game_data)
    print(f"수정 후 경기 숫자: {len(games)}")

    try:
        with open(temp_file_location, "w") as outfile:
            json.dump(games, outfile, ensure_ascii=False)
            print("patch complete!")
    except Exception as e:
        print(e)
