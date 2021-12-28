""" 목표: 매 시합마다 출전하는 KBO 선수들의 선수 id를 크롤링해서 dict(list(dict)) 형식으로 저장하고 table 형태로 정리하기
    
    TODO:
    - [x] 경기 별 등록 선수 목록을 크롤링 하기
    - [x] 등록 선수 목록의 이름을 통해 선수 id 크롤링 하기
    - [x] 선수 id 목록 table로 정리하기
    output
-------
> batter_player = make_table(20210421,20210424,True)
> batter_player
ID	team	이름	현재 상태
51003	51003	KT	권동진	KBO
62415	62415	삼성	박해민	KBO
67341	67341	키움	이정후	KBO
77248	77248	두산	오재원	KBO
79215	79215	두산	박건우	KBO
...	...	...	...	...
HOW TO USE
-------
1. 필요한 라이브러리와 .py 파일을 읽어온다. 
2. 선수 id를 크롤링하는 함수를 정의한다.
3. searching_players 함수 사용시 만약 error_list가 발생한다면 해당 선수들만 다시 크롤링한다.
4. error_list가 없다면 선수들의 id를 make_table() 함수를 사용한다.

"""

from get_players import player_name
import requests
from bs4 import BeautifulSoup 
import configparser
import pandas as pd

config = configparser.ConfigParser()
config.read("config.ini",encoding='utf-8')
player_search_url = eval(config["DEFAULT"]["player_search_URL"])


def searching(name):
    url = f"{player_search_url}{name}"
    r = requests.post(url)
    try:
        soup = BeautifulSoup(r.text, "lxml")
        table = soup.find("table")
        table_rows = table.find_all("a")
        tds = table.find_all("td")
        temp = [parsing_player_table(table_row, tds, num) for num, table_row in enumerate(table_rows)]
        res = [{item["ID"]: item} for item in temp]
    except:
        res = False
    return res


def parsing_player_table(table_row, tds, num):
    idx = 2 + 7*num
    cnt = 4 + 7*num
    if str(table_row).split("/")[1] == "Futures":
        status = "Futures"
    elif str(table_row).split("/")[2] == "Retire":
        status = "은퇴"
    else:
        status = "KBO"
    player_id = str(table_row).split("playerId=")[1].split('">')[0]
    team = tds[idx].get_text()
    name = table_row.get_text()
    birth = tds[cnt].get_text()
    return {"ID": player_id, "이름": name, "생년월일":birth, "현재 상태": status, "team": team}


def searching_players(players_list):
    total = []
    error_list = []
    for name in players_list:
        temp = searching(name)
        if len(temp) == 0:
            error_list.append(name)
        else:
            total += temp
    return {"list": total, "error_list": error_list}


def make_table(start_date, end_date, b_or_p):
    batter_list, pitcher_list = player_name(start_date, end_date)
    if b_or_p == True:
        batter_player_df = pd.DataFrame()
        batter_player = searching_players(batter_list)
        for i in range(len(batter_player["list"])):
            batter_player_df = batter_player_df.append(
                pd.DataFrame(batter_player["list"][i]).T
            )
        return batter_player_df
    else:
        pitcher_player_df = pd.DataFrame()
        pitcher_player = searching_players(pitcher_list)
        for i in range(len(pitcher_player["list"])):
            pitcher_player_df = pitcher_player_df.append(
                pd.DataFrame(pitcher_player["list"][i]).T
            )
        return pitcher_player_df
