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


def changing_win_or_loss_to_int(win_or_loss):
    """승, 패, 무승부를 int 형으로 바꾸는 함수

    Examples:

        ```python
        temp = ["승", "패", "무승부"]
        temp_list = [changing_win_or_loss_to_int(item) for item in temp]
        print(temp_list)
        ```

    Args:
        win_or_loss (str): ["승", "패", "무승부"]와 같은 문자열

    Returns:
        (int): 1 or -1 or 0
    """

    if win_or_loss == "승":
        return 1
    elif win_or_loss == "패":
        return -1
    else:
        return 0


def changing_dbheader_to_bool(dbheader):
    """더블헤더경기인지 아닌지를 int 형으로 바꾸는 함수

    Examples:

        ```python
        temp = ["승", "패", "무승부"]
        temp_list = [changing_win_or_loss_to_int(item) for item in temp]
        print(temp_list)
        ```

    Args:
        win_or_loss (str): ["승", "패", "무승부"]와 같은 문자열

    Returns:
        (int): 1 or -1 or 0
    """

    if win_or_loss == "승":
        return 1
    elif win_or_loss == "패":
        return -1
    else:
        return 0


def changing_dbheader_to_bool(dbheader):
    """더블헤더경기인지 아닌지를 bool 형으로 바꾸는 함수

    Examples:

        ```python
        temp = [0, 1, 2]
        temp_list = [changing_dbheader_to_bool(item) for item in temp]
        print(temp_list)
        ```

    Args:
        dbheader (int)

    Returns:
        (bool): False or True
    """

    if dbheader == 1:
        return True
    else:
        return False


def is_exist_inning(inning_num):
    """해당 이닝에 경기를 했는지 안 했는지 파악하는 함수

    Examples:

        ```python
        temp = [0, 1, 2]
        temp_list = [is_exist_inning(item) for item in temp]
        print(temp_list)
        ```

    Args:
        inning_num (int): 해당 이닝 득점인데, 만약 -1이면 해당 이닝 경기가 없다는 의미

    Returns:
        None, or int
    """

    if inning_num == -1:
        return None
    else:
        return inning_num
