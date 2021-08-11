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

    today_schedule = get_game_schedule.today()
    # 오늘 schedule이 잘 들어왔는지 확인
    print(f"KEY: {KEY}")
