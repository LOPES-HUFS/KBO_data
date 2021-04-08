""" 수집한 KBO 경기 일정을 파싱하는 모듈

KBO 경기 일정을 수집합니다. 오늘 경기 일정은 네이버에서 가져오고 있습니다.

Example:
    오늘 경기 일정은 아래와 같이 실행하면, `2021_04_06_Schedule.json`과 같은 이름으로 
    파일을 만들어 줍니다.

        >>> import parsing_game_schedule
        >>> test = {"year": "2021", "date": "04.06", "1": {"away": "SS", "home": "OB", "state": "18:30"}, "2": {"away": "LT", "home": "NC", "state": "18:30"}, "3": {"away": "LG", "home": "KT", "state": "18:30"}, "4": {"away": "HT", "home": "WO", "state": "18:30"}, "5": {"away": "HH", "home": "SK", "state": "18:30"}}
        >>> parsing_game_schedule.changing_format(test)
        [{'gameDate': '20210406', 'gameld': 'SSOB0'}, {'gameDate': '20210406', 'gameld': 'LTNC0'}, {'gameDate': '20210406', 'gameld': 'LGKT0'}, {'gameDate': '20210406', 'gameld': 'HTWO0'}, {'gameDate': '20210406', 'gameld': 'HHSK0'}]

"""


def chang_name_into_id(team_name, year):
    """팀 이름을 팀 ID로 바꾸는 함수

    2021년 SSG가 창단했다. 그래서 팀명이 SK에서 SSG로 변경되었다.
    그러나 KBO 홈피에서 사용하는 ID는 안 바꾼 것 같다.
    그래서 팀명을 KBO에서 바꾸는 함수를 새로 만들었다.

    Args:
        team_name (str): 팀명

    """

    team_list_2021 = {
        "KIA": "HT",
        "두산": "OB",
        "롯데": "LT",
        "NC": "NC",
        "SSG": "SK",
        "LG": "LG",
        "넥센": "WO",
        "키움": "WO",
        "히어로즈": "WO",
        "우리": "WO",
        "한화": "HH",
        "삼성": "SS",
        "KT": "KT",
    }
    team_list = {
        "KIA": "HT",
        "두산": "OB",
        "롯데": "LT",
        "NC": "NC",
        "SK": "SK",
        "LG": "LG",
        "넥센": "WO",
        "키움": "WO",
        "히어로즈": "WO",
        "우리": "WO",
        "한화": "HH",
        "삼성": "SS",
        "KT": "KT",
    }

    if year == "2021":
        return team_list_2021[team_name]
    else:
        return team_list[team_name]


def changing_format(schedule_dict):
    temp_date = ""
    match_list = []
    results = []

    for item in schedule_dict:
        if item == "year":
            temp_date = schedule_dict[item]
        elif item == "date":
            temp_date = temp_date + "".join(schedule_dict[item].split("."))
        else:
            temp_teams = schedule_dict[item]["away"] + schedule_dict[item]["home"]
            if temp_teams in match_list:
                if schedule_dict[item]["suspended"] == "DH1":
                    results.append(
                        {
                            "gameDate": temp_date,
                            "gameld": (temp_teams + "1"),
                            "state": schedule_dict[item]["state"],
                        }
                    )
                else:
                    results.append(
                        {
                            "gameDate": temp_date,
                            "gameld": (temp_teams + "2"),
                            "state": schedule_dict[item]["state"],
                        }
                    )
            else:
                match_list.append(temp_teams)
                results.append(
                    {
                        "gameDate": temp_date,
                        "gameld": (temp_teams + schedule_dict[item]["suspended"]),
                        "state": schedule_dict[item]["state"],
                    }
                )

    return results
