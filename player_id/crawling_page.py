""" 목표: 매 시합마다 출전하는 KBO 선수들의 이름들을 크롤링해서 문자열 리스트로 생성
    
    TODO:
    - [x] KBO홈페이지에서 요일별로 크롤링하기
    - [x] 데이터 정제하기
    - [x] 문자열 데이터 정규표현식으로 나눠서 이름 리스트 생성하기
    - [x] 각 요일마다 생성된 리스트 이름 기준 고유값으로 저장하기
    - [ ] 리스트의 첫 번째 공백 문자열 제외하는 로직으로 디버그(그냥 결과값에서 인덱스 1로 잡아도 됩니다)

output
-------
> batters, pitchers = player_name("20210422", "20210424")
> batters[:5]
['', '노진혁', '프레이타스', '김지찬', '박병호']
> pitchers[:5]
['', '이준영', '문경찬', '임현준', '최원태']

HOW TO USE
-------
1. 아래의 함수들을 정의한다.
2. player_name()에 크롤링하고 싶은 시작과 끝 년월일을 입력한다.
"""

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import re
import lxml
import pandas as pd
from bs4 import BeautifulSoup as bs
from datetime import datetime

def date_range(start, end):
    start = datetime.strptime(start, "%Y%m%d")
    end = datetime.strptime(end, "%Y%m%d")
    dates = [date.strftime("%Y%m%d") for date in pd.date_range(start, periods=(end-start).days+1)]
    return dates
  
def proprocess_data(result):
    concat = result['포수']+result['내야수']+result['외야수']
    alone = result['투수']
    pitchers=''
    batters=''
    for i in range(len(concat)):
        batters +=  concat[i]
        pitchers += alone[i]
        pitcher = re.split('\(\d+\)',pitchers)
        batter =  re.split('\(\d+\)',batters)
    return pitcher, batter

def player_name(start, end):
    
    dates = date_range(start, end)
    batters = []
    pitchers = []
    
    for date in dates:
        with requests.Session() as s:
            r = s.get('https://www.koreabaseball.com/Player/RegisterAll.aspx', verify=False)
            soup = bs(r.content, 'lxml')
            vs = soup.select_one('#__VIEWSTATE')['value']
            ev = soup.select_one('#__EVENTVALIDATION')['value']
            vsg = soup.select_one('#__VIEWSTATEGENERATOR')['value']
            data = {
                '__LASTFOCUS': '',
                '__VIEWSTATE':vs,
                '__VIEWSTATEGENERATOR': vsg,
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__EVENTVALIDATION': ev,
                'ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$hfSearchDate': date,
                'ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$btnSearch': ''}
            r = requests.post('https://www.koreabaseball.com/Player/RegisterAll.aspx',  data=data)
            soup = bs(r.content, 'lxml')
            tbl = soup.find("table",{'class':"tData tDays"})
            result= pd.read_html(str(tbl))
        pitcher, batter = proprocess_data(result[0])
        batters += batter
        pitchers += pitcher
        batters = list(set(batters))
        pitchers = list(set(pitchers))
    
    return batters, pitchers
