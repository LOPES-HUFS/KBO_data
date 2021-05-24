""" KBO 자료를 다루기 위한 유용한 함수를 가지고 있는 모듈
자료를 수집하고, 이를 파일로 만드는 것과 관련된 코드를 가지고 있다.
물론 다른 곳에서 사용한 코드를 사용하기 때문에 중복되는 기능을 가지고 있기도 하다.

"""
import json
import csv

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
    """수집한 하루 게임 데이터를 월별로 묶는 함수"""
    game_date = {}

    for item in json_file_list:
        with open(item) as json_file:
            json_data = json.load(json_file)
            game_date.update(json_data)

    file_name = "temp_data_" + year_str + "_" + month_str + ".json"

    with open(file_name, "w") as outfile:
        json.dump(game_date, outfile)


def json_merge(main_file_name, sub_file_name):
    """main_file 파일에 sub_file에 들어 있는 자료를 병합하는 함수

    기본적으로 main_file_name 인 json 파일을 dict로 열고
    거기에 sub_file_name 인 jjson 파일을 dict로 열어서 윗쪽 dict에 병합한 다음
    이를 main_file_name으로 입력된 파일에 다시 json 파일로 저장합니다.ㄴ


    Examples:
        ```python
        import utility
        utility.json_merge("temp_data_2021_5.json", "2021_05.07_games.json")
        ```

    Args:
        - main_file_name (json): KBO 게임 내용이 들어 있는 파일 이름
        - sub_file_name (json): KBO 게임 내용이 들어 있는 파일 이름

    """

    with open(main_file_name) as json_file:
        main_json_data = json.load(json_file)

    with open(sub_file_name) as json_file:
        json_data = json.load(json_file)
        main_json_data.update(json_data)

    with open(main_file_name, "w") as outfile:
        json.dump(main_json_data, outfile)


def get_KBO_data(game_list_file_name):
    """csv 형식으로 되어 있는 이미 조사한 KBO 게임 스케줄을 가지고 게임 data를 모으는 함수

    2021년 이전 경기 자료를 새로 수집하기 위한 함수입니다.
    아래 링크에 가시면 "temp_schedule_2020.csv"과 같은 형식의 파일이 게임 스케줄 파일입니다.

    https://github.com/dialektike/KBO/tree/master/data

    이 파일을 이용해서 특정 년도 KBO 경기 자료를 받을 수 있습니다.
    참고로 아래와 같이 이 파일들의 첫 번째 줄은 header 이기 때문에 두 번째 줄부터 이용합니다.

    ```csv
             date gameid
    0    20180324  HHWO0
    1    20180325  HHWO0
    2    20180327  HHNC0
    ```

    그리고 자료를 수집할 때 수집이 안 된 게임 목록은 따로 csv 형식 파일로 만들게 됩니다.
    이 목록을 가지고 다시 수집한다면 완전한 KBO 게임 자료를 구하실 수 있습니다.

    Example:

        ```python
        import utility
        utility.get_KBO_data("temp_schedule_2020.csv")
        ```

    Args:
        game_list (csv): 다음과 같은 게임 스케줄 파일

    """

    game_date = {}
    count = 0
    error_list = []

    with open(game_list_file_name, newline="") as f:
        game_list = csv.reader(f)
        for row in game_list:
            count = count + 1
            if row[0] == "date":
                pass
            else:
                try:
                    print(count, row)
                    game_date.update(get_data.single_game(row[0], row[1]))
                except:
                    error_list.append(row)

    # 수집한 자료를 저장하기 위한 파일 명 만들기
    if game_list_file_name.find("temp_schedule_") != -1:
        file_name = game_list_file_name.replace("schedule", "data")
        file_name = file_name.replace("csv", "json")
    else:
        file_name = "game_data.json"

    with open(file_name, "w") as outfile:
        json.dump(game_date, outfile)

    # 수집하지 못한 경기 리스트를 저장하기 위한 파일 명 만들기
    if game_list_file_name.find("temp_schedule_") != -1:
        error_list_file_name = game_list_file_name.replace(
            "schedule", "schedule_error_list"
        )
    else:
        error_list_file_name = "schedule_error_list.csv"

    with open(error_list_file_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(error_list)
