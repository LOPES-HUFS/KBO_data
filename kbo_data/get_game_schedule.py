""" KBO 경기 일정을 가져오는 모듈

KBO 경기 일정을 수집합니다. 오늘 경기 일정은 네이버에서 가져오고 있습니다.

Example:
    오늘 경기 일정은 `today()`으로 가져 온다음 `modify()`으로 정리합니다.

    >>> import get_game_schedule
    >>> today_schedule = get_game_schedule.today()
    >>> temp = get_game_schedule.modify(today_schedule['list'], today_schedule['date'])
    >>> temp
    {'year': '2021', 'date': '11.04', 1: {'away': 'OB', 'home': 'LG', 'state': '18:30', 'suspended': '0'}}

"""

import configparser
from datetime import date

import requests
from bs4 import BeautifulSoup

import parsing_game_schedule


def today():
    """오늘 경기 일정을 가져오는 함수

    오늘 경기가 없는 경우에는 수집하는 웹 페이지에 오늘 날짜가
    없을 수 있다. 그래서 이전 경기 또는 이후 경가 수집될 수도
    있다. 그리고 정규 시즌인 경우에는 "KBO리그"이라는
    문자열이 있어야 하는데 이것이 없으면 수집할 필요가 없기 때문에
    아래 코드에서 이를 검사해서 자료를 수집하고 있다.
    데이터 분석하기 위해 modify 하기 쉽도록 다운받은 내용 그대로
    유지하면서 내용을 추가하지 않고 필요하지 않은 부분,
    예를 들어 HTML 관련 코드 등을 정리한다.

    Returns
    -------
    False: bool
        만약 반환값이 `False`이면 정구 시즌 경기가 없다는 것이다.

    Json
        - 'status_code': requests status_code
        - 'date': e.g.: '11.04'
        - 'list': e.g.: <li></li>로 수집된 경기 일정 HTML 코드로 되어 있는 리스트

    """

    # 최종 반환값 temp
    temp = {}

    config = configparser.ConfigParser()
    config.read("config.ini", encoding="utf-8")
    temp_url = config["DEFAULT"]["naver_KBO_URL"]
    req = requests.get(temp_url)
    temp["status_code"] = req.status_code
    # print(req.status_code)
    html = req.text

    soup = BeautifulSoup(html, "lxml")
    # 오늘 게임 경기가 있으면 is_KBO_game_schedule = 'KBO리그'이어야 한다.
    is_KBO_game_schedule = soup.find("h2", class_="h_sch").text

    if is_KBO_game_schedule == "KBO리그":
        # 우선 현재 가져온 자료에서  날짜를 찾아 저장한다.
        temp_date = soup.find("li", role="presentation", class_="on").find("em").text
        temp["date"] = temp_date

        daily_schedule = soup.find(
            "div", id="_daily_schedule_root", class_="schedule_slider"
        )
        temp["list"] = []

        for item in daily_schedule.find_all("li"):
            # 경기 일정은 없고 빈 박스만 있는 경우에는 반환 경기 일정 list에 추가하지 않습니다.
            if item.contents == []:
                pass
            else:
                temp["list"].append(item)

        return temp

    else:
        return False


def modify(schedule_list, schedule_date):
    """가져온 오늘 경기 일정을 modify 하는 함수

    `today()`으로 가져온 경기 일정을 사용하기 쉽게 정리하고 고친다.
    최종적으로 저장하고 다루기 쉬운 JSON 형식으로 변형한다.

    Returns
    -------
    False: bool
        만약 반환값이 `False`이면 정구 시즌 경기가 없다는 것이다.

    JSON: e.g.
        temp = {
        "year": "2021",
        "date": "11.04",
        1: {"away": "OB", "home": "LG", "state": "18:30", "suspended": "0"},
        }

    """

    # 최종 반환값 exporting_dict
    exporting_dict = {}

    # 현재 연도를 가져온다.
    today = date.today()
    exporting_dict["year"] = str(today.year)
    exporting_dict["date"] = schedule_date

    i = 1

    for item in schedule_list:
        if item.find("div", class_="vs_cnt").find("p", class_="suspended") == None:
            suspended = "0"
        else:
            temp_suspended = item.find("div", class_="vs_cnt").find(
                "p", class_="suspended"
            )
            suspended = temp_suspended.text.strip()
            if suspended == "DH1":
                suspended = "DH1"
            else:
                suspended = "DH2"

        temp_list = {
            "away": parsing_game_schedule.chang_name_into_id(
                item.find("div", class_="vs_lft").find_all("strong")[0].text,
                exporting_dict["year"],
            ),
            "home": parsing_game_schedule.chang_name_into_id(
                item.find("div", class_="vs_rgt").find_all("strong")[0].text,
                exporting_dict["year"],
            ),
            "state": item.find("div", class_="vs_cnt")
            .find_all("em", class_="state")[0]
            .text.strip(),
            "suspended": suspended,
        }

        exporting_dict[i] = temp_list

        i = i + 1

    return exporting_dict
