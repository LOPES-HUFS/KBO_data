""" github actions을 이용해서 오늘 KBO 경기 자료를 모으는 모듈

   이 모듈을 github action을 통해서 자동적으로 작동하게끔 만들어졌다.

"""

import sys
from datetime import date
import json

import pandas as pd
import requests
import sqlalchemy as db

import get_data
import get_game_schedule
import parsing_game_schedule
import scoreboards

if __name__ == "__main__":

    today = date.today()

    temp_date = f"{today.month}.{today.day}"

    post_json = {
        "key": "get",
        "value": {"year": str(today.year), "date": temp_date},
    }
    # print(post_json)

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
            print(f'{item["gameDate"]}: 게임 자료 수집 완료!')
        else:
            print(item["state"])

    temp_scoreboards = scoreboards.output_to_dict(game_date)

    print(temp_scoreboards)

    # DB 설정 시작
    DB_URL = str(sys.argv[2])

    engine = db.create_engine(DB_URL)
    connection = engine.connect()
    metadata = db.MetaData()
    # DB에 스코어 보드 자료 입력 시작
    table = db.Table("scoreboard", metadata, autoload=True, autoload_with=engine)
    print(f"table columns keys:{table.columns.keys()}")

    query = db.insert(table)
    result_proxy = connection.execute(query, temp_scoreboards)
    result_proxy.close()
    # DB에 스코어 보드 자료 입력 완료
