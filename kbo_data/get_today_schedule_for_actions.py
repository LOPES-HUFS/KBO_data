""" github actions을 이용해서 오늘 KBO 경기 자료를 모으는 모듈

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
    DB_URL = str(sys.argv[2])

    engine = db.create_engine(DB_URL)
    connection = engine.connect()
    metadata = db.MetaData()
    table = db.Table('scoreboard', metadata, autoload=True, autoload_with=engine)
    print(table.columns.keys())


    #today_schedule = get_game_schedule.today()
    # 오늘 스케줄이 들어왔다고 가정한다.
    today_schedule = {
        "year": "2021",
        "date": "08.10",
        "1": {"away": "SK", "home": "LG", "state": "\uc885\ub8cc", "suspended": "0"},
        "2": {"away": "OB", "home": "SS", "state": "\ucde8\uc18c", "suspended": "0"},
        "3": {"away": "LT", "home": "NC", "state": "\uc885\ub8cc", "suspended": "0"},
        "4": {"away": "KT", "home": "WO", "state": "\uc885\ub8cc", "suspended": "0"},
        "5": {"away": "HH", "home": "HT", "state": "\uc885\ub8cc", "suspended": "0"},
    }
    # 오늘 schedule이 잘 들어왔는지 확인
    print(f"Today_schedule: {today_schedule}")
    game_schedule = parsing_game_schedule.changing_format(today_schedule)
    print(f"game_schedule: {game_schedule}")

    game_date = {}

    for item in game_schedule:
        if item["state"] == "종료":
            temp_data = get_data.single_game(item["gameDate"], item["gameld"])
            temp = scoreboards.output_to_tuples(temp_data)
            print(temp)
        else:
            print(item["state"])