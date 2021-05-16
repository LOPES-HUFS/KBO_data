
## Proof of concept about database schema

```bash
                          [Scoreboards]
[TeamID]                 - idx(key)  ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅣ
- teamID(key) ㅡㅡㅡㅡㅡ - TeamID(foreign key)           ㅣ
- name                                                   ㅣ
                                                         ㅣ
                          [Batters]                      ㅣ
[PlayerID]                - idx(foreign key) ㅡㅡㅡㅡㅡㅡㅣ
- playerID(key)ㅡㅣㅡㅡㅡ - playerID(foreign key)        ㅣ
- name           ㅣ                                      ㅣ
                 ㅣ       [Pitchers]                     ㅣ
                 ㅣ       - idx(foreign key) ㅡㅡㅡㅡㅡㅡㅣ
                 ㅣㅡㅡㅡ - playerID(foreign key)       
```
