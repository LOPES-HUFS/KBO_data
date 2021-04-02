import configparser
import json

from selenium import webdriver
from bs4 import BeautifulSoup

if __name__ == "__main__":

    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        temp_url = config["DEFAULT"]["naver_KBO_URL"]
        chromium_location = config["DEFAULT"]["chromium_location"]

        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("window-size=1920x1080")
        options.add_argument("disable-gpu")
        # 혹은 options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(chromium_location, options=options)
        driver.get(url=temp_url)

        exporting_dict = {}

        driver.implicitly_wait(3)
        soup = BeautifulSoup(driver.page_source, "lxml")

        exporting_dict = {}

        # 우선 현재 가져온 자료를 날짜를 찾는다.
        temp_date = soup.find("li", role="presentation", class_="on").find("em").text
        exporting_dict["date"] = temp_date
    
        # 다음으로 게임 상대를 찾는다.
        todaySchedule = soup.find_all("ul", id="todaySchedule")
        temp_todaySchedule = todaySchedule[0]

        i = 0
        for item in temp_todaySchedule.find_all("li"):
            i = i + 1
            temp_list = [
                item.find("div", class_="vs_lft").find_all("strong")[0].text,
                item.find("div", class_="vs_rgt").find_all("strong")[0].text,
            ]
            exporting_dict[i] = temp_list
        # print(exporting_dict)
        file_name = temp_date.replace(".", "_") + "_Schedule.json"
        with open(file_name, "w") as outfile:
            json.dump(exporting_dict, outfile)

    except Exception as e:
        print(e)    
        driver.quit()

    finally:
        print("finally...")
        driver.quit()