from datetime import date
import json

import pandas as pd

import get_data
# import get_game_schedule
import parsing_game_schedule

if __name__ == "__main__":

    test = {"year": "2021", "date": "04.06", 
            "1": {"away": "SS", "home": "OB", "state": "종료"}, 
            "2": {"away": "LT", "home": "NC", "state": "종료"}, 
            "3": {"away": "LG", "home": "KT", "state": "종료"}, 
            "4": {"away": "HT", "home": "WO", "state": "종료"}, 
            "5": {"away": "HH", "home": "SK", "state": "18:30"}}

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

#    single_game_to_json("20210404", "LTSK0")
    game_schedule =  parsing_game_schedule.changing_format(test)
    for item in game_schedule:
        if item['state'] == "종료":
            single_game_to_json(item['gameDate'], item['gameld'])
        else:
            print(item['state'])

