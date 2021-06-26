""" 특정 년도 특정 월 KBO 경기 일정을 가져오는 모듈

KBO 홈페이지에서 KBO 경기 일정을 수집합니다.
특정 년도, 특정 월의 경기 일정을 get_data

Example:
    `get_data()` 경기 일정만을 가져옵니다.
    이를 사용하기 쉽게 만들기 위해서는 `modify_data()`를 사용해야 합니다.

        >>> import get_monthly_game_schedules
        >>> temp = get_monthly_game_schedules.get(2021, 5, "정규")
        >>> temp = get_monthly_game_schedules.modify(2021, temp)
        >>> temp
                 date away home gameid
        0    20210501   SK   OB  SKOB0
        1    20210501   HH   LT  HHLT0
        2    20210501   LG   SS  LGSS0
        3    20210501   WO   NC  WONC0
        4    20210501   HT   KT  HTKT0
        ..        ...  ...  ...    ...
        108  20210530   WO   LG  WOLG0
        109  20210530   NC   LT  NCLT0
        110  20210530   OB   SS  OBSS0
        111  20210530   KT   HT  KTHT0
        112  20210530   SK   HH  SKHH0

"""

import time
from datetime import datetime
import re
import configparser

from selenium import webdriver
import pandas as pd


config = configparser.ConfigParser()
# 설정파일을 읽어옵니다.
config.read("config.ini")
Game_info_URL = config["DEFAULT"]["Game_info_URL"]
chromium_location = config["DEFAULT"]["chromium_location"]

team_list = eval(config["DEFAULT"]["team_list"])


def change_team_name(string):
    """팀명을 코드로 바꿔 주는 함수.

    만약 팀명이 없는 경우에는 '없음'를 되돌려 준다.

    Arg:
        팀명 : (str)
    Returns:
        팀 코드
    """

    try:
        return team_list[string]

    except:
        print(string)
        return "없음"


def get(year, month, season):
    """특정 연도에 특정 월에 했던 KBO 경기 스케줄을 가져오는 함수

    Args:
        year (int): 년도
        month (int): 월
        season (str): '시범', '정규', '포스트' 중 하나를 선택

    Returns:
        (df) 게임 일정
    """

    if season == "시범":
        season = 1
    elif season == "정규":
        season = "0,9"
    else:
        season = "3,4"

    month = str(month).zfill(2)

    try:
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("window-size=1920x1080")
        options.add_argument("disable-gpu")
        url = Game_info_URL + season
        driver = webdriver.Chrome(chromium_location, chrome_options=options)
        driver.get(url)
        time.sleep(1)
        driver.find_element_by_id("ddlYear").send_keys(year)
        time.sleep(1)
        driver.find_element_by_id("ddlMonth").send_keys(month)
        time.sleep(1)
        table = driver.find_element_by_css_selector("table")
        gamelist = []
        for row in table.find_elements_by_css_selector("tr"):
            gamelist.append([d.text for d in row.find_elements_by_css_selector("td")])

        del gamelist[0]

        [
            gamelist[i].insert(0, gamelist[i - 1][0])
            for i in range(0, len(gamelist))
            if len(gamelist[i]) == 8
        ]
        if gamelist[0][0] == "데이터가 없습니다.":
            return (
                "Please check the date, there are no games in the month of that year."
            )
        else:
            gamelist_df = pd.DataFrame(
                gamelist,
                columns=["날짜", "시간", "경기", "게임센터", "하이라이트", "TV", "라디오", "구장", "비고"],
            )

    except Exception as e:
        print(e)

    finally:
        print("finally...")
        driver.quit()

    return gamelist_df


def modify(year, data):
    """
    입력값: data는 get_game_info_table 함수의 return 값
    출력값: 날짜 원정팀, 홈팀 gameid가 포함된 DF
    """

    data = data[
        (data["비고"] != "우천취소")
        & (data["비고"] != "강풍취소")
        & (data["비고"] != "그라운드사정")
        & (data["비고"] != "기타")
        & (data["비고"] != "미세먼지취소")
    ]

    gameinfo = [s.split("vs") for s in data["경기"]]
    awayteam = []
    hometeam = []
    for i in gameinfo:
        awayteam.append("".join(re.findall("[^0-9]", i[0])))
        hometeam.append("".join(re.findall("[^0-9]", i[1])))

    homecode = [change_team_name(i) for i in hometeam]
    awaycode = [change_team_name(i) for i in awayteam]

    date = [
        str(year) + i.split(".")[0] + "".join(re.findall("[0-9]", i.split(".")[1]))
        for i in data["날짜"]
    ]

    gameid = [awaycode[i] + homecode[i] + "0" for i in range(0, len(awaycode))]
    gameid_list = pd.DataFrame(
        {"date": date, "away": awaycode, "home": homecode, "gameid": gameid}
    )

    double_header = gameid_list.index[gameid_list.duplicated(keep=False) == True]

    one = [i for i in range(0, len(double_header)) if i % 2 == 1]
    gameid_list.gameid[double_header[one]] = [
        str(i).replace("0", "2") for i in gameid_list.gameid[double_header[one]]
    ]
    gameid_list.gameid[
        double_header[[x for x in range(0, len(double_header)) if x not in one]]
    ] = [
        str(i).replace("0", "1")
        for i in gameid_list.gameid[
            double_header[[x for x in range(0, len(double_header)) if x not in one]]
        ]
    ]

    gameid_list = gameid_list[gameid_list["home"] != "없음"]
    gameid_list = gameid_list.reset_index(drop=True)

    return gameid_list


def output_to_csv(data):
    """수집한 월 게임 일정을 사용하기 쉽게 `csv` 형식의 파일로 바꾸는 함수

    Args:
        data (df): 아래와 같은 형식의 월 스케줄

        ```csv
                 date away home gameid
        0    20210501   SK   OB  SKOB0
        1    20210501   HH   LT  HHLT0
        ```

    Example:

        ```python
        import get_monthly_game_schedules
        temp = get_monthly_game_schedules.get(2021, 5, "정규")
        temp = get_monthly_game_schedules.modify(2021, temp)
        get_monthly_game_schedules.output_to_csv(temp)
        ```

    Output:

        ```csv
            date,gameid
        20210501,SKOB0
        20210501,HHLT0
        20210501,LGSS0
        20210501,WONC0
        20210501,HTKT0
        20210502,SKOB0
        20210502,HHLT0
        20210502,LGSS0
        ...
        ```

    """

    temp_date = pd.to_datetime(data["date"], format="%Y%m%d")

    if all(temp_date.dt.month):
        temp_year = str(temp_date[1].year)
        temp_month = str(temp_date[1].month).zfill(2)
        temp_main = "game_schedule_"
        temp_file_name = temp_main + temp_year + "_" + temp_month + ".csv"
        data.to_csv(
            temp_file_name,
            sep=",",
            na_rep="NaN",
            columns=["date", "gameid"],
            index=False,
        )
    else:
        print("같은 월 경기 스케줄만 있는 것이 아닙니다!")
