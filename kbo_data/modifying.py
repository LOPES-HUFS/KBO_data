"""수집된 KBO 자료를 정리할 때 사용하는 모듈

   수집한 자료를 정리(modify)할 때, 
   한 곳이 아니라 여러 곳에서 사용하는 코드들을 모아둔 모듈입니다.

   - `changing_team_name_into_id()` : 팀명을 팀 id로 바꾸는 함수
   - 

"""
import configparser

# 설정파일을 읽어옵니다.
config = configparser.ConfigParser()
config.read("config.ini")


def changing_team_name_into_id(team_name):
    """팀명을 팀 TeamID로 바꾸는 함수

    Examples:

        ```python
        import modifying
        modifying.changing_team_name_into_id("두산")
        '1'
        ```

    Args:
        team_name (str): 팀명

    Returns:
        (str): 자연수 숫자
    """

    return config["TEAM"][team_name]
