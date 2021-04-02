import get_data
import pandas as pd
import json

if __name__ == "__main__":

    def single_game_to_json(gameDate, gameld):
        """
        단일 게임 페이지를 받아서 JSON 파일로 저장하는 함수

        :param gameDate: "20181010" 와 같이 경기 날짜를 문자열로 받는다.

        :param gameld: 경기를 하는 팀명으로 만들어진다.
        "WOOB0"과 같이 만드는데, WO, OB는 각각 팀명을 의미하고
        0은 더블헤더 경기가 아닌 것을 알려준다.
        만약 더불헤더 경기면 1차전은 "KTLT1"처럼 1로 표시하고
        2차전이면 "KTLT2"으로 표시한다.
        사용법은 get_data.single_game과 같다.
        """

        temp_page = get_data.single_game(gameDate, gameld)

        with open("test.json", "w") as outfile:
            json.dump(temp_page, outfile)

    single_game_to_json("20181010", "KTLT1")
