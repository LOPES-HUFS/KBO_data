import pandas as pd


def scoreboard(tables, teams):
    temp_df_0 = pd.read_html(str(tables[0]))[0]
    temp_df_0 = temp_df_0.rename(columns={"Unnamed: 0": "승패"})
    temp_df_1 = pd.read_html(str(tables[1]))[0]
    temp_df_2 = pd.read_html(str(tables[2]))[0]
    temp_teams_df = pd.DataFrame({"팀": teams})
    temp_total = pd.concat(
        [temp_teams_df, temp_df_0["승패"], temp_df_1, temp_df_2], axis=1
    )
    return temp_total


def looking_for_team_name(string):
    # team_list={'HT':'기아','OB':'두산','LT':'롯데','NC':'NC','SK':'SK','LG':'LG','WO':'넥센','HH':'한화','SS':'삼성','KT':'KT'}
    # 2019년 버전
    team_list = {
        "HT": "기아",
        "OB": "두산",
        "LT": "롯데",
        "NC": "NC",
        "SK": "SK",
        "LG": "LG",
        "WO": "키움",
        "HH": "한화",
        "SS": "삼성",
        "KT": "KT",
    }
    temp = [string.find(team) for team in team_list.keys()]
    temp[:] = [0 if ele != -1 else ele for ele in temp]
    # -1: 없다 이고 나머지 숫자는 그것이 있는 자리다!
    temp = temp.index(0)
    temp = list(team_list.items())[temp]
    return temp[1]


def looking_for_teams_name(teams):
    temp_0 = looking_for_team_name(str(teams[0]))
    temp_1 = looking_for_team_name(str(teams[1]))
    return (temp_0, temp_1)


def looking_for_team_names(temp_teams):
    """ 모은 HTML soup에서 시합한 두 팀명을 뽑는 함수 

    다음과 같은 HTML soup에서  "한화"만 뽑아서 팀명을 찾는다.

    실제로는 아래와 같은 것이 두 팀에서 각 각 타자, 투수 총 네 번 나온다.
    거기서 두 팀만 뽑으면 된다. 또한 아래처럼 "한화 이글스 타자 기록"에서 첫 번째 단어만 뽑으면 된다.

    <h6 class="tit-team" id="lblAwayHitter">
        <span class="logo">
            <img src="//lgcxydabfbch3774324.cdn.ntruss.com \ 
            /KBO_IMAGE/emblem/regular/2020/initial_HH_s.png" alt="한화 이글스">
        </span>
    한화 이글스 타자 기록</h6>

        Args:
            temp_teams (soup): 위에서 보여준 html soup

        Returns:
            temp_data (tuple): (두산, LG)처럼 `str`형식으로 두 팀 명,
                                첫 번째 팀이 원정팀(두산), 두 번째 팀(LG)은 홈팀
    """
    temp_team_list = []

    for team in temp_teams:
        temp_team = team.get_text()
        temp_team = temp_team.split(" ")
        if (temp_team[0] in temp_team_list) == False:
            temp_team_list.append(temp_team[0])

    return (temp_team_list[0], temp_team_list[1])


def etc_info(tables, record_etc):
    record = {}
    header_list = tables[3].find_all("th")
    if len(header_list) != 0:
        header = [h.get_text(strip=True) for h in header_list]
        data = tables[3].find_all("td")
        etc_data = [d.get_text(strip=True) for d in data]
        record = {header[i]: etc_data[i] for i in range(0, len(header))}
        record.update(
            {
                key: record[key].split(") ")
                for key in record.keys()
                if len(record[key].split(") ")) >= 2
            }
        )
        record["심판"] = record["심판"].split(" ")
    etc = {
        record_etc[0]
        .find_all("span")[i]
        .get_text()
        .split(" : ")[0]: record_etc[0]
        .find_all("span")[i]
        .get_text()
        .split(" : ")[1]
        for i in range(0, len(record_etc[0].find_all("span")))
    }
    # etc={i.split(" : ")[0]:i.split(" : ")[1] for i in record_etc[0].get_text().split("\n") if len(i)!=0 }
    record.update(etc)
    return record


def away_batter(tables, team):
    temp1 = pd.read_html(str(tables[4]))[0].dropna()
    temp1 = temp1.rename(columns={"Unnamed: 1": "포지션"})
    del temp1["Unnamed: 0"]
    temp2 = pd.read_html(str(tables[5]))[0][:-1]
    temp3 = pd.read_html(str(tables[6]))[0][:-1]
    away = pd.concat([temp1, temp2, temp3], axis=1)
    away["팀"] = team[0]
    away = away.fillna(0)
    return away


def home_batter(tables, team):
    temp1 = pd.read_html(str(tables[7]))[0].dropna()
    temp1 = temp1.rename(columns={"Unnamed: 1": "포지션"})
    del temp1["Unnamed: 0"]
    temp2 = pd.read_html(str(tables[8]))[0][:-1]
    temp3 = pd.read_html(str(tables[9]))[0][:-1]
    home = pd.concat([temp1, temp2, temp3], axis=1)
    home["팀"] = team[1]
    home = home.fillna(0)
    return home


def away_pitcher(tables, team):
    away = pd.read_html(str(tables[10]))[0][:-1]
    away["팀"] = team[0]
    away = away.fillna(0)
    return away


def home_pitcher(tables, team):
    home = pd.read_html(str(tables[11]))[0][:-1]
    home["팀"] = team[1]
    home = home.fillna(0)
    return home
