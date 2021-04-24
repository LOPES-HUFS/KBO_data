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
        pitchers = list(set(batters))
    
    return batters, pitchers
