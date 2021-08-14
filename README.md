# KBO_data

## 목표

KBO 데이터를 가져와서 정리해 데이터 분석을 하기 쉽게 만드는 코드를 작성하고자 합니다.

## 사용 방법

현재 이 프로젝트는 `python 3.7`을 기준으로 작성하고 있습니다. 이 버젼 이상을 사용하시면 무리없이 작동할 것입니다.

### 오늘 게임 스케줄 정보 가져오기

오늘 KBO 경기 스케줄 정보를 가져 오려면 다음과 같이 하면 됩니다. 조심할 점은 경기 없는 날은, 다음 경기가 있는 날짜의 정보를 가져옵니다.

```python
>>> import get_game_schedule
>>> today_schedule = get_game_schedule.today()
200
>>> print(today_schedule)
{'year': '2021', 'date': '04.10', 1: {'away': 'SK', 'home': 'LG', 'state': '6회초', 'suspended': '0'}, 2: {'away': 'KT', 'home': 'SS', 'state': '5회말', 'suspended': '0'}, 3: {'away': 'WO', 'home': 'LT', 'state': '17:00', 'suspended': '0'}, 4: {'away': 'OB', 'home': 'HH', 'state': '17:00', 'suspended': '0'}, 5: {'away': 'NC', 'home': 'HT', 'state': '17:00', 'suspended': '0'}}
```

### 특정 일자 경기 정보 가져오기

다음과 같이 특정 일자 경기 스케줄 정보가 있다면, 이를 가지고 경기 정보를 다음과 같은 방법으로 가져올 수 있습니다. 가져온 자료는 입력된 경기 스케줄 정보를 토대로 저장 파일명을 만들어서 가져온 자료를 `json` 형식의 파일로 저장하게 됩니다. 현재 `temp_schedule`에 `"year": "2021", "date": "04.08"`라고 명시되어 있기 때문에 `2021_04.08_games.json`이라는 파일 이름을 만들어서 저장하게 됩니다.

```python
temp_schedule = {"year": "2021", "date": "04.08", "1": { "away": "SS", "home": "OB", "state": "종료", "suspended": "0" }, "2": { "away": "LT", "home": "NC", "state": "종료", "suspended": "0" }, "3": { "away": "LG", "home": "KT", "state": "종료", "suspended": "0" },"4": { "away": "HT", "home": "WO", "state": "종료", "suspended": "0" },"5": { "away": "HH", "home": "SK", "state": "종료", "suspended": "0" }}
import utility
utility.get_one_day_data_to_json(temp_schedule)
```

### 특정 년도 특정 월 경기 정보 가져오기

우선 2021년 7월 정규시즌 경기 자료를 모으려면, 우선 해당 기간의 스케줄을 모아야 합니다. 아래와 같은 코드를 입력하시면 됩니다. 그러면 스케줄 정보가 `csv` 형식 파일로 만들어 집니다. 참고로 `output_to_csv()`은 temp_schedule_2021_07 과 같은 형식으로 파일 이름을 자동으로 만들어서 파일로 저장합니다.

```python
import get_monthly_game_schedules
temp = get_monthly_game_schedules.get(2021, 7, "정규")
temp = get_monthly_game_schedules.modify(2021, temp)
# 위에서 저장한 수집한 스케줄을 csv 형식으로 파일로 저장합니다.
import utility
get_monthly_game_schedules.output_to_csv(temp)
```

앞에서 만든 `csv` 형식 파일로 경기 자료를 수입해 보겠습니다. 아래와 같이 하시면, 경기 자료가 `game_data.json`이라는 파일 이름으로 저장됩니다.

```python
import utility
utility.get_KBO_data("temp_schedule_2021_07.csv")
```

### 일일 경기 파일 합쳐서 월 경기 묶음 파일로 만들기

앞에서 가져온 일일 경기 자료 파일을 합쳐서 월 경기 자료로 파일로 만듭니다. 현재는 아래와 같이 함수 인수에 연도와 월을 입력하면 이를 토대로 파일 이름을 `temp_data_2021_4.json`과 같이 만들어서 저장하게 됩니다.

```python
temp_list = ["2021_04.03_games.json", "2021_04.04_games.json", "2021_04.06_games.json", "2021_04.07_games.json", "2021_04.08_games.json", "2021_04.09_games.json", "2021_04.10_games.json"]

import utility
utility.binding_json(temp_list, "2021", "4")
```

## 코드 작성시 참고할 점

앞에서도 언급한 것처럼 현재 코드는 `python 3.7`을 기준으로 작성하고 있습니다. 그리고 `poetry`를 이용해서 파이썬 관련 패키지를 관리하고 있습니다.

### 코드 정리

코드 정리는 `black`을 이용하여 아래와 같이 해주시면 됩니다.

```bash
python -m black get_data.py
```

### poetry 설치

맥에서는 아래와 같이 설치하시면 됩니다.

```bash
brew install poetry
```

### 파이썬 가상 환경 설정

맥에도 `python 3`이 설치되어 있으니 안정적으로 사용하기 위해서 파이썬 가상 환경을 만들어서 사용하시는 편이 좋습니다. 맥에서 `python 3.7` 가상 환경을 만드는 방법은 아래와 `pyenv`과 `pyenv-virtualenv`을 설치하신 다음,

```bash
brew install pyenv
brew install pyenv-virtualenv
pyenv install 3.7.9
```

아래왜 같이 설치된 것을 확인한 다음,

```bash
ls ~/.pyenv/versions/
3.7.9
```

`KBO_dev`라는 가상 환경을 만드신 다음 이 가상 환경을 아래와 같이 활성화(activate)하시면 됩니다. 참고로 활성화를 취소하려면 `deactivate`을 사용하시면 됩니다.

```bash
pyenv virtualenv 3.7.9 KBO_dev
pyenv activate KBO_dev
pyenv deactivate
```

만약 잘 안 되는 경우에는 아래와 같은 `poetry` 명령어로 `virtualenvs.path`을 변경해주시면 됩니다.

```bash
poetry config virtualenvs.path /Users/pi/.pyenv/versions/3.7.9/envs/KBO_dev
```

주의할 점은 `/Users/pi/.pyenv/versions/3.7.9/envs/KBO_dev` 부분은 터미널에서 `pyenv virtualenvs`을 입력했을 때, `3.7.9/envs/KBO_dev (created from /Users/pi/.pyenv/versions/3.7.9)`을 참고해서 입력하시면 됩니다. 아래 실행 결과를 참고하세요!

```bash
❯ pyenv virtualenvs
  3.7.9/envs/KBO_dev (created from /Users/pi/.pyenv/versions/3.7.9)
  3.9.1/envs/poetry_test (created from /Users/pi/.pyenv/versions/3.9.1)
* KBO_dev (created from /Users/pi/.pyenv/versions/3.7.9)
  poetry_test (created from /Users/pi/.pyenv/versions/3.9.1)
```
