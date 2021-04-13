""" KBO 자료를 다루기 위한 유용한 함수를 가지고 있는 모듈
자료를 수집하고, 이를 파일로 만드는 것과 관련된 코드를 가지고 있다.
물론 다른 곳에서 사용한 코드를 사용하기 때문에 중복되는 기능을 가지고 있기도 하다.

"""
import json

import get_data
import get_game_schedule
from parsing_game_schedule import changing_format

def get_one_day_data_to_json(input_schedule):

    game_schedule = changing_format(input_schedule)
    
    game_date = {}

    for item in game_schedule:
        print(item)
        if item["state"] == "종료":
            game_date.update(get_data.single_game(item["gameDate"], item["gameld"]))
        else:
            print(item["state"])

    file_name = input_schedule["year"] + "_" + input_schedule["date"] + "_games.json"

    with open(file_name, "w") as outfile:
        json.dump(game_date, outfile)

def binding_json(json_file_list, year_str, month_str):
    """수집한 하루 게임 데이터를 월별로 묶는 함수
    """
    game_date = {}

    for item in json_file_list:
        with open(item) as json_file:
            json_data = json.load(json_file)
        game_date.update(json_data)

    file_name = "temp_data_" + year_str + "_" + month_str + ".json"

    with open(file_name, "w") as outfile:
        json.dump(game_date, outfile)

def json_merge(main_file_name, sub_file_name):
    """
    두 파일을 열어서 앞 main_file 파일에 sub_file를 파일을 병합하는 함수
    """

    with open(main_file_name) as json_file:
        main_json_data = json.load(json_file)

    with open(sub_file_name) as json_file:
        json_data = json.load(json_file)
        main_json_data.update(json_data)

    file_name = main_file_name

    with open(file_name, "w") as outfile:
        json.dump(main_json_data, outfile)
