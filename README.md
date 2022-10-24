# KBO_data

## 목표

KBO 데이터를 가져와서 정리해 데이터 분석을 하기 쉽게 만드는 파이썬 스크립트를 작성하고자 합니다.

## 사용 방법

현재 이 프로젝트는 `conda`를 사용하여 `python 3.8`으로 가상환경을 구성하여 작동하는 것을 원칙으로 하고 있습니다. 그리고 현재 이 프로젝트에는 `selenium`, 버전 '4.x' 이상을 요구하는 코드가 있습니다. `selenium`을 '3.x' 버젼으로 사용하시면 작동하지 않을 수 있습니다. 이와 같은 조건을 충족하기 위해서는 가상 환경을 설치하고 이 프로젝트에서 필요한 패키지를 설치하는 방법은 강추합니다. 아래 내용을 참고하시면 손쉽게 이 프로젝트에서 사용하고 있는 가상환경올 구축할 수 있습니다.

### `conda`를 시용하여 가상 환경을 만들고 패키지 설치하기

앞에서는 이 프로젝트를 사용하기 위해서는 `python 3.8`이 필요합니다. 여기서는 [miniforge](https://github.com/conda-forge/miniforge)를 사용할 것입니다. **miniforge** 설치는 다음 링크를 참고하세요.

- [conda-forge-miniforge- A conda-forge distribution](https://github.com/conda-forge/miniforge#download)

그러면 `conda`를 이용하여 이 프로젝트에서 사용할 가상 환경을 만들어 보겠습니다.

```console
conda create -n kbo_data python=3.8
conda activate kbo_data
```

1번째 줄은 `kbo_data`이라는 이름으로 가상 환경을 만드는 것이고 2번째 줄은 그 가상 환경을 활성화하는 것입니다. 이제 앞에서 만든 `kbo_data`이라는 가상 환경에 이 프로젝트에서 필요한 패키지를 설치해 보겠습니다. `black`은 이 프로젝트의 코드를 작성하고 나서 코드를 정리하는 패키지입니다.

```console
conda install requests
conda install pandas
conda install selenium
conda install bs4
conda install lxml
conda install black
```

만약 가상환경에서는 나가시려면 `deactivate`를 아래와 같이 사용하면 되고, 앞에서 설치한 `kbo_data`이라는 가상환경을 제거하려면 `remove`를 아래와 같이 사용하면 됩니다.

```console
conda deactivate
conda remove -n kbo_data --all
```

### 프로젝트 파일 실행 방법

실행하기 위해서는 우선 아래와 같이 프로젝트 폴더가 보이는 상태에서 터미널이나 윈도우에서는 윈도우 콘솔 또는 cmd을 시작합니다.

```console
README.md       kbo_data        league-schedule public          sample_data     schema
```

그런 다음 다음과 같이 폴더를 이동하여 앞에서 만든 가상 환경을 활성화 한 다음 본 프로젝트의 파이썬 코드를 실행하면 됩니다.

```console
cd kbo_data
conda activate kbo_data
python
```

### 오늘 게임 스케줄 정보 가져오기

오늘 KBO 경기 스케줄 정보를 가져 오려면 다음과 같이 하면 됩니다. 조심할 점은 경기 없는 날은, 다음 경기가 있는 날짜의 정보를 가져옵니다. 다음은 작동 화면입니다.

```python
>>> import get_game_schedule
>>> temp = get_game_schedule.today()
>>> if temp['status_code'] == 200:
...     today_schedule = get_game_schedule.modify(temp['list'], temp['date'])
... else:
...     print("game schedule download failed")
... 
>>> today_schedule
# 아래 출력은 실행하는 날짜에 따라서 다르게 나옵니다.
# 참고하세요.
{
    "year": "2021",
    "date": "04.10",
    1: {"away": "SK", "home": "LG", "state": "6회초", "suspended": "0"},
    2: {"away": "KT", "home": "SS", "state": "5회말", "suspended": "0"},
    3: {"away": "WO", "home": "LT", "state": "17:00", "suspended": "0"},
    4: {"away": "OB", "home": "HH", "state": "17:00", "suspended": "0"},
    5: {"away": "NC", "home": "HT", "state": "17:00", "suspended": "0"},
}
```

### 특정 일자 경기 정보 가져오기

다음과 같이 특정 일자 경기 스케줄 정보가 있다면, 이를 가지고 경기 정보를 다음과 같은 방법으로 가져올 수 있습니다. 가져온 자료는 입력된 경기 스케줄 정보를 토대로 저장 파일명을 만들어서 가져온 자료를 `json` 형식의 파일로 저장하게 됩니다. 현재 `temp_schedule`에 `"year": "2021", "date": "04.08"`라고 명시되어 있기 때문에 `2021_04.08_games.json`이라는 파일 이름을 만들어서 저장하게 됩니다.

```python
temp_schedule = {
    "year": "2021",
    "date": "04.08",
    "1": {"away": "SS", "home": "OB", "state": "종료", "suspended": "0"},
    "2": {"away": "LT", "home": "NC", "state": "종료", "suspended": "0"},
    "3": {"away": "LG", "home": "KT", "state": "종료", "suspended": "0"},
    "4": {"away": "HT", "home": "WO", "state": "종료", "suspended": "0"},
    "5": {"away": "HH", "home": "SK", "state": "종료", "suspended": "0"},
}
import utility
utility.get_one_day_data_to_json(temp_schedule)
```

### 특정 년도 특정 월 경기 정보 가져오기

우선 2021년 7월 정규시즌 경기 자료를 모으려면, 우선 해당 기간의 스케줄을 모아야 합니다. 아래와 같은 코드를 입력하시면 됩니다. 그러면 스케줄 정보가 `csv` 형식 파일로 만들어 집니다. 참고로 `output_to_csv()`은 temp_schedule_2021_07 과 같은 형식으로 파일 이름을 자동으로 만들어서 파일로 저장합니다.

```python
import get_monthly_game_schedules
temp = get_monthly_game_schedules.get(2022, 10, "정규")
temp = get_monthly_game_schedules.modify(2022, temp)
# 위에서 저장한 수집한 스케줄을 csv 형식으로 파일로 저장합니다.
import utility
get_monthly_game_schedules.output_to_csv(temp)
```

앞에서 만든 `csv` 형식 파일로 경기 자료를 수집해 보겠습니다. 아래와 같이 하시면, 경기 자료가 `game_data.json`이라는 파일 이름으로 저장됩니다.

```python
import utility
utility.get_KBO_data("game_schedule_2022_10.csv")
```

### 일일 경기 파일 합쳐서 월 경기 묶음 파일로 만들기

앞에서 가져온 일일 경기 자료 파일을 합쳐서 월 경기 자료로 파일로 만듭니다. 현재는 아래와 같이 함수 인수에 연도와 월을 입력하면 이를 토대로 파일 이름을 `temp_data_2021_4.json`과 같이 만들어서 저장하게 됩니다.

```python
temp_list = [
        "2021_04.03_games.json",
        "2021_04.04_games.json",
        "2021_04.06_games.json",
        "2021_04.07_games.json",
        "2021_04.08_games.json",
        "2021_04.09_games.json",
        "2021_04.10_games.json",
    ]

import utility
utility.binding_json(temp_list, "2021", "4")
```

## 한계점

이 프로젝트를 이용하면 2008년 이후 자료만 수집하는 것을 추천합니다. 왜냐하면 그 이전 자료는 수집할 수 없는 경기가 너무 많기 때문이다. 그리고 아래 4 게임도 자료를 수집할 수 없습니다.

1. 2018년 8월 1일, 우리(현 키움) vs. SK(현 SSG)
2. 2015년 7월 8일, 기아 vs. 우리(현 키움)
3. 2009년 4월 4일 ,우리(현 키움) vs. 롯데
4, 2008년 3월 30일,롯데 vs. 한화"

## 코드 정리

만약 이 프로젝트에 문제가 있는 코드를 고치시거나 개선해서 코드를 '풀 리퀘스트(pull request)'를 하시려는 분이 있다면 아래와 같이 `black`을 이용하여 정리해 '풀 리퀘스트'를 해주시면 고맙겠습니다.

```bash
python -m black get_data.py
```
