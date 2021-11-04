""" github actions을 이용해서 오늘 KBO 경기 자료를 모으는 모듈

"""

import sys
import json

import requests

import get_game_schedule

if __name__ == "__main__":

    temp = get_game_schedule.today()
    if temp['status_code'] == 200:
        today_schedule = get_game_schedule.modify(temp['list'], temp['date'])
    else:
        print("game schedule download failed")

    #today_schedule = get_game_schedule.today()

    # 연습용 today_schedule dict
    # today_schedule = {
    #     "year": "2021",
    #     "date": "08.11",
    #     1: {"away": "SK", "home": "LG", "state": "종료", "suspended": "0"},
    #     2: {"away": "OB", "home": "SS", "state": "종료", "suspended": "0"},
    #     3: {"away": "LT", "home": "NC", "state": "종료", "suspended": "0"},
    #     4: {"away": "KT", "home": "WO", "state": "종료", "suspended": "0"},
    #     5: {"away": "HH", "home": "HT", "state": "종료", "suspended": "0"},
    # }

    # 연습용 temp_value dict
    # 주석처리 하지 않고 그냥 쓰지 않습니다.
    temp_value = {
        "value": {
            "year": "2021",
            "date": "08.33",
            "1": {"away": "SK", "home": "LG", "state": "18:30", "suspended": "0"},
            "2": {"away": "OB", "home": "SS", "state": "18:30", "suspended": "0"},
            "3": {"away": "LT", "home": "NC", "state": "18:30", "suspended": "0"},
            "4": {"away": "KT", "home": "WO", "state": "18:30", "suspended": "0"},
            "5": {"away": "HH", "home": "HT", "state": "18:30", "suspended": "0"},
        }
    }

    # print(f"Today_schedule: {today_schedule}")

    url = str(sys.argv[1])

    post_json = {
        "key": "get",
        "value": {"year": today_schedule["year"], "date": today_schedule["date"]},
    }

    try:
        # 가장 최근 경기 스케줄을 가져옵니다.
        r = requests.post(url, data=json.dumps(post_json))
        get_json = r.json()
        latest_list = eval(get_json["body"])
        # print(f"Latest_saved_game_schedule: {latest_list}")
        # 오늘 경기 스케줄과 가장 최근 저장된 스케줄을 비교해 다르면
        # 오늘 경기 스케줄 저장합니다.
        if today_schedule == latest_list:
            print(f"오늘 것과 최근 것이 같다?: {today_schedule == latest_list}")
            pass
        elif today_schedule == False:
            print(f"오늘 KBO 경기 스케줄 있지?: {today_schedule}")
            pass
        else:
            temp_put_data = {"key": "put"}
            temp_dict = {"value": today_schedule}
            temp_put_data.update(temp_dict)
            # 아래 코드 1줄을 연습용 코드
            # temp_put_data.update(temp_value)
            print(f"putting_data: {temp_put_data}")
            r = requests.post(url, data=json.dumps(temp_put_data))
            # 저장이 잘 되었으면 {"statusCode": 200, "body": "put done"} 나옴
            print(f"put?: {r.text}")

    except Exception as e:
        print(e)
