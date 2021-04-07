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
                results.append(
                    {
                        "gameDate": temp_date,
                        "gameld": (temp_teams + "1"),
                        "state": schedule_dict[item]["state"],
                    }
                )
            else:
                match_list.append(temp_teams)
                results.append(
                    {
                        "gameDate": temp_date,
                        "gameld": (temp_teams + "0"),
                        "state": schedule_dict[item]["state"],
                    }
                )

    return results
