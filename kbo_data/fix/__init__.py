""" KBO 자료에서 부족한 것들을 수정 보완하는 라이브러리
수집한 수집한 장소의 자료가 누락되거나 잘못되어 있어 이 프로젝트 코드로 모은 KBO 자료도 
당연히 누락되거나 잘못되어 있는 자료가 있다.
이 모듈이 이를 보완하기 위한 것이다. 이 모듈은 다른 곳에 있는 자료를 가지고 여기서 모은 
자료를 보완한다.
"""

import csv

from . import fix_season_2009


def season_2009(location):
    # fix_season_2009.team_names(location)
    fix_season_2009.pitchers_data()


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
