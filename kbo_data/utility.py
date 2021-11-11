""" KBO 자료를 다루기 위한 유용한 함수를 가지고 있는 모듈
자료를 수집하고, 이를 파일로 만드는 것과 관련된 코드를 가지고 있다.
물론 다른 곳에서 사용한 코드를 사용하기 때문에 중복되는 기능을 가지고 있기도 하다.

"""
import json
import csv

import get_page
from parsing_game_schedule import changing_format


def get_one_day_data_to_dict(input_schedule):
    """input_schedule으로 들어온 게임 스케줄을 가지고 게임 자료를 수집하는 함수

    기본적으로 input_schedule을 통해 1개 이상의 게임 스케줄이 들어옵니다.
    이를 가지고 게임 자료를 수입해서 이를 dict로 반환합니다.

    Examples:
        ```python
        temp_schedule = {
            "year": "2021",
            "date": "04.08",
            "1": {"away": "SS", "home": "OB", "state": "종료", "suspended": "0"},
            "2": {"away": "LT", "home": "NC", "state": "종료", "suspended": "0"},
            "3": {"away": "LG", "home": "KT", "state": "종료", "suspended": "0"},
            "4": {"away": "HT", "home": "WO", "state": "종료", "suspended": "0"},
            "5": {"away": "HH", "home": "SK", "state": "종료", "suspended": "0"},
        }

        import utility
        temp_data = utility.get_one_day_data_to_dict(temp_schedule)
        ```

    Args:
        - input_schedule (dict): 특정 날짜의 KBO 경기 스케줄, 형식은 위에

    Returns:
        game_date (dict): 입력된 input_schedule을 가지고 수입한 KBO 경기 자료

    """

    game_schedule = changing_format(input_schedule)
    game_schedule = [item for item in game_schedule if item["state"] == "종료"]

    game_date = []

    for item in game_schedule:
        game_date.append(get_page.single_game(item["gameDate"], item["gameld"]))

    return game_date


def get_one_day_data_to_json(input_schedule):

    game_schedule = changing_format(input_schedule)

    game_date = []

    for item in game_schedule:
        print(item)
        if item["state"] == "종료":
            game_date.append(get_page.single_game(item["gameDate"], item["gameld"]))
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

    game_date = []
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
                    game_date.append(get_page.single_game(row[0], row[1]))
                    print(f"No. {count}, ID: {row}, Download completed.")
                except:
                    print(f"No. {count}, ID: {row}, Download Failed.")
                    error_list.append(row)

    # 수집한 자료를 저장하기 위한 파일 명 만들기
    if game_list_file_name.find("temp_schedule_") != -1:
        file_name = game_list_file_name.replace("schedule", "data")
        file_name = file_name.replace("csv", "json")
    else:
        file_name = "game_data.json"

    with open(file_name, "w") as outfile:
        json.dump(game_date, outfile, ensure_ascii=False)

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


def get_one_day_game_data():
    """2021년 4월 8일자 KBO 경기 자료를 가져오는 함수

    코딩 테스트를 위하여 하루치 경기를 인터넷에서 가져옵니다.

    Example:

        ```python
        import utility
        temp_data = utility.get_one_day_game_data()
        ```

    Returns:
        game_date (dict): 2021년 4월 8일자 KBO 경기 자료

    """

    temp_schedule = {
        "year": "2021",
        "date": "04.08",
        "1": {"away": "SS", "home": "OB", "state": "종료", "suspended": "0"},
        "2": {"away": "LT", "home": "NC", "state": "종료", "suspended": "0"},
        "3": {"away": "LG", "home": "KT", "state": "종료", "suspended": "0"},
        "4": {"away": "HT", "home": "WO", "state": "종료", "suspended": "0"},
        "5": {"away": "HH", "home": "SK", "state": "종료", "suspended": "0"},
    }

    game_schedule = changing_format(temp_schedule)

    game_date = []

    for item in game_schedule:
        print(item)
        if item["state"] == "종료":
            game_date.append(get_page.single_game(item["gameDate"], item["gameld"]))
        else:
            print(item["state"])

    return game_date
