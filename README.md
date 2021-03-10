# KBO_data

## 목표

KBO 데이터를 가져와서 정리해 데이터 분석을 하기 쉽게 만드는 코드를 작성하고자 합니다.

## 사용 방법

현재 이 프로젝트는 `python 3.7`을 기준으로 작성하고 있습니다. 이 버젼 이상을 사용하시면 무리없이 작동할 것입니다.

## 코드 작성시 참고할 점

앞에서도 언급한 것처럼 현재 코드는 `python 3.7`을 기준으로 작성하고 있습니다. 그리고 `poetry`를 이용해서 파이썬 관련 패키지를 관리하고 있습니다.

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

`KBO_dev`라는 가상 환경을 만드신 다음 이 가상 환경을 아래와 같이 활성화(activate)하시면 됩니다.

```bash
pyenv virtualenv 3.7.9 KBO_dev
pyenv activate KBO_dev
```

### 코드 정리

코드 정리는 `black`을 이용하여 아래와 같이 해주시면 됩니다.

```bash
python -m black get_data.py
```
