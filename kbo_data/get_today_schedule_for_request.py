"""오늘 경기 일정을 가져오는 모듈

네이버에서 오늘 경기를 가져오는 모듈입니다.

Example:
    아래와 같이 실행하면, `2021_04_06_Schedule.json`과 같은 이름으로 
    파일을 만들어 줍니다.

        $ python get_today_schedule_for_request.py

TODO:
    - 현재 파일을 만들고 있지만, 그냥 함수로 만들어서
      경기 자료를 바로 받아올 수 있게 바꾸면 될 것 같습니다.

"""

import configparser
import json
from datetime import date

import requests
from bs4 import BeautifulSoup

import pasing_page

if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read("config.ini")
    temp_url = config["DEFAULT"]["naver_KBO_URL"]
    req = requests.get(temp_url)
    print(req.status_code)
    html = req.text

    exporting_dict = {}

    soup = BeautifulSoup(html, "lxml")

    exporting_dict = {}

    # 현재 연도를 가져온다.
    today = date.today()
    exporting_dict["year"] = str(today.year)

    # 우선 현재 가져온 자료를 날짜를 찾는다.
    temp_date = soup.find("li", role="presentation", class_="on").find("em").text
    exporting_dict["date"] = temp_date
    
    # 다음으로 게임 상대를 찾는다.
    todaySchedule = soup.find_all("ul", id="todaySchedule")
    temp_todaySchedule = todaySchedule[0]

    i = 0
    for item in temp_todaySchedule.find_all("li"):
        i = i + 1
        temp_list = {
            "away":
            pasing_page.chang_name_into_id_2021(
                item.find("div", class_="vs_lft").find_all("strong")[0].text
            ),
            "home":
            pasing_page.chang_name_into_id_2021(
                item.find("div", class_="vs_rgt").find_all("strong")[0].text
            ),
            "state":
            item.find("div", class_="vs_cnt").find_all("em", class_="state")[0].text.strip()
        }
        exporting_dict[i] = temp_list

    #print(exporting_dict)
    file_name = str(today.year) + "_" + temp_date.replace(".", "_") + "_Schedule.json"

    with open(file_name, "w") as outfile:
        json.dump(exporting_dict, outfile)
