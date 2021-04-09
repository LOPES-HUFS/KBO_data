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

if __name__ == "__main__":

    def single_game_to_json(gameDate, gameld):
        """
        단일 게임 페이지를 받아서 JSON 파일로 저장하는 함수

        :param gameDate: "20181010" 와 같이 경기 날짜를 문자열로 받는다.

        :param gameld: 경기를 하는 팀명으로 만들어진다.
        "WOOB0"과 같이 만드는데, WO, OB는 각각 팀명을 의미하고
        0은 더블헤더 경기가 아닌 것을 알려준다.
        만약 더불헤더 경기면 1차전은 "KTLT1"처럼 1로 표시하고
        2차전이면 "KTLT2"으로 표시한다.

        Example:
            single_game_to_json("20210404", "LTSK0")
        """

        temp_page = get_data.single_game(gameDate, gameld)

        # 파일 이름을 만들기 위하여 문자열을 생성한다.
        temp = gameDate + "_" + gameld
        # 자료가 잘 들어왔는지 스코어보드를 인쇄한다.
        print(temp_page[temp]["scoreboard"])
        # 전체 파일명을 만든다.
        file_name = temp + ".json"

        with open(file_name, "w") as outfile:
            json.dump(temp_page, outfile)

    today_schedule = get_game_schedule.today()
    # 오늘 schedule이 잘 들어왔는지 확인
    print(today_schedule)
    game_schedule = parsing_game_schedule.changing_format(today_schedule)

    url = str(sys.argv[1])

    post_json = {"year": "2021", "date": "04.04"}

    r = requests.post(url, data = json.dumps(post_json))
    print(r.json)

    game_date = {}

    for item in game_schedule:
        if item["state"] == "종료":
            single_game_to_json(item["gameDate"], item["gameld"])
            game_date.update(get_data.single_game(item["gameDate"], item["gameld"]))
        else:
            print(item["state"])

    file_name = today_schedule["year"] + "_" + today_schedule["date"] + "_games.json"

    with open(file_name, "w") as outfile:
        json.dump(game_date, outfile)
