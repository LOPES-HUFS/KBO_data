import ast
import configparser
import json

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

from pasing_page import scoreboard, etc_info, looking_for_team_names
from pasing_page import away_batter, home_batter, away_pitcher, home_pitcher


config = configparser.ConfigParser()
# 설정파일을 읽어옵니다.
config.read("config.ini", encoding='utf-8')
# 설정파일에 들어있는 KBO url을 가져 옵니다.
url = config["DEFAULT"]["KBO_URL"]
chromium_location = config["DEFAULT"]["chromium_location"]


def getting_page(gameDate, gameld):
    """
    단일 게임 페이지를 chromium를 다운받아서 단순하게 자료를 분류하는 함수다.
    속도를 조금이나마 빠르게 하기 위해서 lxml을 사용하고 있다.
    driver.implicitly_wait(3) : 이 정도 기다려야 페이지를 잘 받을 수 있다.

    :param gameDate: "20181010" 와 같이 경기 날짜를 문자열로 받는다.

    :param gameld: 경기를 하는 팀명으로 만들어진다.
        "WOOB0"과 같이 만드는데, WO, OB는 각각 팀명을 의미하고
        0은 더블헤더 경기가 아닌 것을 알려준다.
        만약 더불헤더 경기면 1차전은 "KTLT1"처럼 1로 표시하고
        2차전이면 "KTLT2"으로 표시한다.
    사용법::
        >>> temp_page=getting_page("20181010","KTLT1")

    Returns:
        (json): 리스트에 들어 있는 전체 
    """
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("window-size=1920x1080")
        options.add_argument("disable-gpu")
        # 혹은 options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(chromium_location, chrome_options=options)
        temp_url = url + gameDate + "&gameId=" + gameDate + gameld + "&section=REVIEW"
        driver.get(temp_url)
        driver.implicitly_wait(5)
        soup = BeautifulSoup(driver.page_source, "lxml")
        tables = soup.find_all("table")
        record_etc = soup.findAll("div", {"class": "record-etc"})
        box_score = soup.findAll("div", {"class": "box-score-wrap"})
        
        # 2021년 5월 12일 현재, h6는 팀 명에서만 사용한다.
        temp_teams = soup.findAll("h6")
        teams = looking_for_team_names(temp_teams)

        return {
            "tables": tables,
            "record_etc": record_etc,
            "teams": teams,
            "date": gameDate,
            "id": gameld,
        }

    except Exception as e:
        print(e)

    finally:
        print("finally...")
        driver.quit()


def single_game(date, gameld):
    temp_page = getting_page(date, gameld)
    temp_scoreboard = scoreboard(temp_page["tables"], temp_page["teams"])
    print(temp_scoreboard)

    temp_all = {
        "scoreboard": ast.literal_eval(temp_scoreboard.to_json(orient="records"))
    }
    temp_all.update(
        {"ETC_info": etc_info(temp_page["tables"], temp_page["record_etc"])}
    )
    temp_all.update(
        {
            "away_batter": ast.literal_eval(
                away_batter(temp_page["tables"], temp_page["teams"]).to_json(
                    orient="records"
                )
            )
        }
    )
    temp_all.update(
        {
            "home_batter": ast.literal_eval(
                home_batter(temp_page["tables"], temp_page["teams"]).to_json(
                    orient="records"
                )
            )
        }
    )
    temp_all.update(
        {
            "away_pitcher": ast.literal_eval(
                away_pitcher(temp_page["tables"], temp_page["teams"]).to_json(
                    orient="records"
                )
            )
        }
    )
    temp_all.update(
        {
            "home_pitcher": ast.literal_eval(
                home_pitcher(temp_page["tables"], temp_page["teams"]).to_json(
                    orient="records"
                )
            )
        }
    )

    temp_name = temp_page["date"] + "_" + temp_page["id"]
    return {temp_name: temp_all}
