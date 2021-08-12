""" github actions을 이용해서 오늘 KBO 경기 자료를 모으는 모듈


Example:
    오늘 경기 일정은 아래와 같이 실행하면, `2021_04_06_Schedule.json`과 같은 이름으로 
    파일을 만들어 줍니다.

    test = {
        "year": "2021",
        "date": "04.06",
        "1": {"away": "SS", "home": "OB", "state": "종료"},
        "2": {"away": "LT", "home": "NC", "state": "종료"},
        "3": {"away": "LG", "home": "KT", "state": "종료"},
        "4": {"away": "HT", "home": "WO", "state": "종료"},
        "5": {"away": "HH", "home": "SK", "state": "18:30"},
    }

        ❯ python for_actions.py
        finally...
        [{'팀': '삼성', '승패': '패', '1': 0, '2': 0, '3': 0, '4': 0, '5': 1, '6': 0, '7': 0, '8': 0, '9': '2', '10': '-', '11': '-', '12': '-', 'R': 3, 'H': 9, 'E': 1, 'B': 1}, {'팀': '두산', '승패': '승', '1': 0, '2': 1, '3': 0, '4': 1, '5': 1, '6': 0, '7': 0, '8': 3, '9': '-', '10': '-', '11': '-', '12': '-', 'R': 6, 'H': 8, 'E': 0, 'B': 5}]
        finally...
        [{'팀': '롯데', '승패': '승', '1': 0, '2': 0, '3': 4, '4': 0, '5': 1, '6': 0, '7': 0, '8': 0, '9': 5, '10': '-', '11': '-', '12': '-', 'R': 10, 'H': 15, 'E': 0, 'B': 5}, {'팀': 'NC', '승패': '패', '1': 0, '2': 0, '3': 1, '4': 0, '5': 2, '6': 1, '7': 1, '8': 0, '9': 0, '10': '-', '11': '-', '12': '-', 'R': 5, 'H': 8, 'E': 3, 'B': 4}]
        finally...
        [{'팀': 'LG', '승패': '승', '1': 0, '2': 0, '3': 2, '4': 0, '5': 0, '6': 0, '7': 0, '8': 1, '9': 0, '10': '-', '11': '-', '12': '-', 'R': 3, 'H': 4, 'E': 1, 'B': 1}, {'팀': 'KT', '승패': '패', '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 2, '9': 0, '10': '-', '11': '-', '12': '-', 'R': 2, 'H': 4, 'E': 2, 'B': 4}]
        finally...
        [{'팀': '기아', '승패': '승', '1': 0, '2': 0, '3': 0, '4': 0, '5': 1, '6': 1, '7': 1, '8': 0, '9': 1, '10': 0, '11': 1, '12': '-', 'R': 5, 'H': 13, 'E': 0, 'B': 3}, {'팀': '키움', '승패': '패', '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 4, '7': 0, '8': 0, '9': 0, '10': 0, '11': 0, '12': '-', 'R': 4, 'H': 5, 'E': 2, 'B': 3}]
        18:30
"""

import sys
from datetime import date
import json

import pandas as pd
import requests

import get_data
import get_game_schedule
import parsing_game_schedule
import scoreboards

if __name__ == "__main__":

    url = str(sys.argv[1])

    today = date.today()

    temp_date = f"{today.month}.{today.day}"

    post_json = {
        "key": "get",
        "value": {"year": str(today.year), "date": temp_date},
    }
    #print(post_json)

    url = str(sys.argv[1])

    r = requests.post(url, data=json.dumps(post_json))
    get_json = r.json()
    game_schedule_list = eval(get_json["body"])
    game_schedule = parsing_game_schedule.changing_format(game_schedule_list)
    # print(f"get game schedule:{game_schedule}")

    game_date = {}

    for item in game_schedule:
        if item["state"] == "종료":
            game_date.update(get_data.single_game(item["gameDate"], item["gameld"]))
        else:
            print(item["state"])

    temp = scoreboards.output_to_dict(game_date)
    #print(temp)
    file_name = "KBO_scoreboards.json"
    
    with open(file_name, "w") as outfile:
        json.dump(temp, outfile)