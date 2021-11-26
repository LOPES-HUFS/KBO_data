""" github actions을 이용해서 오늘 KBO 경기 자료를 모으는 모듈

   이 모듈을 github action을 통해서 자동적으로 작동하게끔 만들어졌다.
"""

import sys
from datetime import date
import json

import requests
import sqlalchemy as db

import get_page
import parsing_game_schedule
import scoreboards
import pitchers
import batters

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
    print(f"get game schedule:{game_schedule}")
    # 종료된 게임 스케줄만 뽑아냅니다.
    game_schedule = [item for item in game_schedule if item["state"] == "종료"]
    print(f"종료된 game schedule:{game_schedule}")

    game_date = []

    for item in game_schedule:
        try:
            if item["state"] == "종료":
                game_date.append(get_page.single_game(item["gameDate"], item["gameld"]))
                print(f'{item["gameDate"]}, {item["gameld"]} : 게임 자료 수집 완료!')
            else:
                print(item["state"])
        except Exception as e:
            print(e)

    print("자료 정리 시작")
    config = configparser.ConfigParser()
    config.read("code_list.ini", encoding="utf-8")
   
    temp_scoreboards = scoreboards.output_to_dict(game_date)
    temp_pitchers = pitchers.output(game_date)
    temp_batters = batters.output(config["BATTER"], game_date)
    print("자료 정리 완료 & 정리한 자료 보기")
    print(temp_scoreboards)
    print(temp_pitchers)
    print(temp_batters)
    print("테이터 받고 정리하고 변환하는 작업 완료")

    # DB 설정 시작
    if len(temp_scoreboards) == 0:
        print("DB에 입력할 자료가 없습니다!")
        pass
    else:
        DB_URL = str(sys.argv[2])

        engine = db.create_engine(DB_URL)
        connection = engine.connect()
        metadata = db.MetaData()
        # DB에 스코어 보드 자료 입력 시작
        table = db.Table("scoreboard", metadata, autoload=True, autoload_with=engine)
        print(f"table columns keys:{table.columns.keys()}")

        query = db.insert(table)

       ## 수정 필요: TypeError: '<' not supported between instances of 'str' and 'int'
       
        result_proxy = connection.execute(query, temp_scoreboards)
        result_proxy.close()
        # DB에 스코어 보드 자료 입력 완료
