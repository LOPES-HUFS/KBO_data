
## Proof of concept about database schema

### schema
```bash
                          [Scoreboards]
                         - idx(key)--------------------ㅣ
                         - Teamname                    ㅣ
                                                       ㅣ
                                                       ㅣ
                          [Batters]                    ㅣ
[PlayerID]                - idx(foreign key) ----------ㅣ
- playerID(key) -ㅣ------ - playerID(foreign key)       ㅣ
- team           ㅣ                                     ㅣ
- name           ㅣ       [Pitchers]                    ㅣ
                 ㅣ       - idx(foreign key) -----------ㅣ
                 ㅣ------ - playerID(foreign key)
```

### environment

- mariaDB in docker container
- os: ubuntu

### 부가설명

위의 스키마가 구현 가능한지를 체크합니다.

- create_table: 위 스키마를 구현한 테이블들을 생성하는 쿼리입니다. 테스트 테이블의 경우 키에 해당하지 않는 컬럼들은 간소화하였습니다.
- insert_data: 만들어진 테이블에 테스트에 사용할 데이터를 생성하는 쿼리입니다.
- test_query: 필요한 데이터가 결과값으로 잘 나오는지 확인하는 쿼리입니다.
