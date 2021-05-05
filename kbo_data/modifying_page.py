""" 가져온 KBO 자료를 가져와서 적절하게 정리하고 DB나 파일로 저장하기 위한 모듈


연습용 json 파일 다운받기

```
wget https://gist.github.com/dialektike/\
761a6053b0c231316a87818aec87a4a7/raw/2021_04.29_games.json
```

사용 방법

```python
    import json
    file_name = "2021_04.29_games.json"
    temp_data = {}
    with open(file_name) as json_file:
            temp_data = json.load(json_file)
    import modifying_page
    temp = modifying_page.input_data(temp_data)
    temp_scoreboards = modifying_page.output(temp)
    ```
"""

import json

import scoreboards


def input_data(data):
    return scoreboards.modify(data)

def output(data):
    return scoreboards.output(data)