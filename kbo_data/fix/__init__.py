""" KBO 자료에서 부족한 것들을 수정 보완하는 라이브러리
수집한 수집한 장소의 자료가 누락되거나 잘못되어 있어 이 프로젝트 코드로 모은 KBO 자료도 
당연히 누락되거나 잘못되어 있는 자료가 있다.
이 모듈이 이를 보완하기 위한 것이다. 이 모듈은 다른 곳에 있는 자료를 가지고 여기서 모은 
자료를 보완한다.
"""

import csv

from . import fix_season_2009


def season_2009(location):
    """2009년 시즌 자료를 수정 보완하는 코드

    2009년 시즌 자료에서는 다음을 수정한다.

    - `fix_team_names()`을 이용하여 팀 이름이 잘못되어 있는 것을 고친다.
    - 4월 4일 서울(현 키움)과 롯데 경기(20090404,WOLT0)에 타자 자료가 없는 것을 추가한다.

    """
    fix_season_2009.changing_team_names(location)
    fix_season_2009.game_data(location)


def changing_str_to_list_in_csv(str_in_csv):
    """`str` 형식으로 된 자료를 csv.reader을 이용해서 분리해 `list` 형식으로 반환하는 함수

    csv 형식이지만 `str`으로 저장된 자료에서 csv.reader을 이용해서
    그 안에 들어 있는 각각의 요소를 분리해서 `list` 형식으로 반환한다.


    Args:
        str_in_csv (str) : 실제로는 `csv` 형식이다.

    Returns:
        temp_list (dict): 각 요소는 `csv` 형식으로 되어 있다.
    """

    temp_list = []
    reader = csv.reader(str_in_csv.split("\n"), delimiter=",")
    for row in reader:
        temp_list.append(row)
    return temp_list


def batters_data(batters_text, batters_patch):
    """타자 자료를 추가하는 함수

    이 프로젝트에서 수집한 자료에 없는 타자 자료를 추가하고자 한다.

    Args:
        - batters_text (str) : 안에 `csv` 형식으로 자료를 저장하고 있다.
        - batters_patch (dict) : 위 text 자료에 넣지 못한 것을 가지고 있다.

    Returns:
        temp_dict (json): 투수 자료
    """
    temp_batters = changing_naver_batters_col_name_and_position(batters_text)
    temp = changing_str_to_list_in_csv(temp_batters)
    temp = changing_naver_batters_list_to_dict(temp, batters_patch)
    temp_dict = {}
    temp_dict[batters_patch["home_or_away"]] = temp
    return temp_dict


def changing_naver_batters_col_name_and_position(batters_text):
    """추가할 타자 자료에 있는 키와 포지션 명을 수집한 자료와 같은 것으로 변경하는 함수

    여기서 추가하려는 자료가 가지고 있는 키 표지션 명이 이 프로젝트 코드로 수집한 것과 다르다.
    이를 동일하게 맞추기 여기에 저장되어 있는 자료에서 키와 포지션 명을 변경한다.
    참고로 자료는 `str` 형식으로 저장되어 있다.

    Args:
        pitchers_text (str): `str` 형식으로 된 타자 자료가 여러 개가 들어 있다.

    Returns:
        temp_pitchers (str): `str` 형식으로 된 타자 자료가 여러 개가 들어 있다.
    """

    # 아래 첫번째 줄 코드는 트릭이다. 자료를 저장할 때 보기 좋게 하기 위해서
    # 맨 윗 줄과 맨 아랫 줄에 넣은 엔터를 제거하는 것이다.
    temp_batters = batters_text[1:-1]
    temp_batters = temp_batters.replace("타자명", "선수명")
    temp_batters = temp_batters.replace("1루수", "一")
    temp_batters = temp_batters.replace("1루", "一")
    temp_batters = temp_batters.replace("2루수", "二")
    temp_batters = temp_batters.replace("2루", "二")
    temp_batters = temp_batters.replace("3루수", "三")
    temp_batters = temp_batters.replace("3루", "三")
    temp_batters = temp_batters.replace("유격수", "유")
    temp_batters = temp_batters.replace("유격", "유")
    temp_batters = temp_batters.replace("우익수", "우")
    temp_batters = temp_batters.replace("우익", "우")
    temp_batters = temp_batters.replace("중견수", "중")
    temp_batters = temp_batters.replace("중견", "중")
    temp_batters = temp_batters.replace("좌익수", "좌")
    temp_batters = temp_batters.replace("좌익", "좌")
    temp_batters = temp_batters.replace("지명타자", "지")
    temp_batters = temp_batters.replace("포수", "포")
    temp_batters = temp_batters.replace("대타", "대")
    temp_batters = temp_batters.replace("·", "")

    return temp_batters


def changing_naver_batters_list_to_dict(batters_list, batters_patch):
    """타자 자료 형식을 `list`에서 `dict`으로 변경하고 추가할 내용을 넣어 정리하는 함수

    자료 중 `이닝`이라는 키로 들어 있는 이닝 자료를 변경하고자 한다.
    다음과 같은 방법으로 이닝을 변경한다.

    Args:
        - batters_list (list): 여러 명의 타자 자료가 들어 있다.
        - batters_patch (dict):

    Returns:
        temp_batters (list): `dict` 형식으로 들어 있는 타자 자료가 여러 개가 들어 있다.
    """

    total_batters_list = []

    for batter in batters_list[1:]:
        i = 0
        temp_data = {}
        for item in batter:
            temp_data["팀"] = batters_patch["팀"]
            temp_data[batters_list[0][i]] = item
            i = i + 1
        total_batters_list.append(temp_data)

    # 특정 회에 값이 없는 경우, 0을 넣는다.
    for temp_batter in total_batters_list:
        for key, value in temp_batter.items():
            if value == "":
                temp_batter[key] = 0

    return total_batters_list


def changing_naver_pitchers_col_name(pitchers_text):
    """추가할 투수 자료에 있는 키를 수집한 자료와 같은 키로 변경하는 함수

    여기서 추가하려는 자료가 가지고 있는 키와 이 프로젝트 코드로 수집한 자료의 키가 다르다.
    이를 동일하게 맞추기 여기에 저장되어 있는 자료에서 키를 변경한다.
    참고로 자료는 `str` 형식으로 저장되어 있다.

    Args:
        pitchers_text (str): `str` 형식으로 된 투수 자료가 여러 개가 들어 있다.

    Returns:
        temp_pitchers (str): `str` 형식으로 된 투수 자료가 여러 개가 들어 있다.
    """

    # 아래 첫번째 줄 코드는 트릭이다. 자료를 저장할 때 보기 좋게 하기 위해서
    # 맨 윗 줄과 맨 아랫 줄에 넣은 엔터를 제거하는 것이다.
    temp_pitchers = pitchers_text[1:-1]
    temp_pitchers = temp_pitchers.replace("투수명", "선수명")
    temp_pitchers = temp_pitchers.replace("승리", "승")
    temp_pitchers = temp_pitchers.replace("패전", "패")
    temp_pitchers = temp_pitchers.replace("세이브", "세")
    temp_pitchers = temp_pitchers.replace("피홈런", "홈런")
    temp_pitchers = temp_pitchers.replace("평균자책", "평균자책점")

    return temp_pitchers


def changing_naver_pitchers_list_to_dict(pitchers_list, pitchers_patch):
    """투수 자료 형식을 `list`에서 `dict`으로 변경하고 추가할 내용을 넣어 정리하는 함수

    투수 자료 중 `이닝`이라는 키로 들어 있는 이닝 자료를 변경하고자 한다.
    다음과 같은 방법으로 이닝을 변경한다.

    Args:
        - pitchers_list (list): 여러 명의 투수 자료가 들어 있다.
        - pitchers_patch (dict):

    Returns:
        temp_pitchers (list): `dict` 형식으로 들어 있는 투수 자료가 여러 개가 들어 있다.
    """

    total_pitchers_list = []

    for pitcher in pitchers_list[1:]:
        i = 0
        temp_data = {}
        for item in pitcher:
            temp_data["팀"] = pitchers_patch["팀"]
            temp_data[pitchers_list[0][i]] = item
            i = i + 1
        if temp_data["선수명"] in pitchers_patch.keys():
            if len(pitchers_patch[temp_data["선수명"]]) == 2:
                temp_data["등판"] = pitchers_patch[temp_data["선수명"]]["등판"]
                temp_data["결과"] = pitchers_patch[temp_data["선수명"]]["결과"]
            else:
                if "등판" in pitchers_patch[temp_data["선수명"]]:
                    temp_data["등판"] = pitchers_patch[temp_data["선수명"]]["등판"]
                    temp_data["결과"] = 0
                else:
                    temp_data["등판"] = 0
                    temp_data["결과"] = pitchers_patch[temp_data["선수명"]]["결과"]
        total_pitchers_list.append(temp_data)
    return total_pitchers_list


def changing_naver_pitchers_inning_format(temp_pitchers):
    """투수 이닝 형식을 변경하는 함수

    투수 자료 중 `이닝`이라는 키로 들어 있는 이닝 자료를 변경하고자 한다.
    다음과 같은 방법으로 이닝을 변경한다.

    ```python
    >>> temp = "2 ⅔"
    >>> temp.replace("⅔","2\\/3")
    '2 2\\/3'
    ```

    Args:
        temp_pitchers (list): `dict` 형식으로 들어 있는 투수 자료가 여러 개가 들어 있다.

    Returns:
        temp_pitchers (list): `dict` 형식으로 들어 있는 투수 자료가 여러 개가 들어 있다.
    """

    for item in temp_pitchers:
        # print(item['이닝'])
        item["이닝"] = item["이닝"].replace("⅓", "1\\/3")
        item["이닝"] = item["이닝"].replace("⅔", "2\\/3")
        item["이닝"] = item["이닝"].replace("0 ", "")
    return temp_pitchers
