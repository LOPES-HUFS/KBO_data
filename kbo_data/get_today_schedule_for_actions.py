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

if __name__ == "__main__":
    today_schedule = get_game_schedule.today()
    # 오늘 schedule이 잘 들어왔는지 확인
    print(today_schedule)
    print()
    game_schedule = parsing_game_schedule.changing_format(today_schedule)

    url = str(sys.argv[1])

    post_json = {
        "year": today_schedule["year"],
        "date": today_schedule["date"],
        "is_latest": "True",
    }
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    r = requests.post(url, headers=headers, data=json.dumps(post_json))
    print(r.json())