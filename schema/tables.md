
# Tables schema

```bash
                          [Scoreboards]
                         - idx(key)--------------------ㅣ
                         - Team_name                   ㅣ
                                                       ㅣ
                                                       ㅣ
                          [Batters]                    ㅣ
[PlayerID]                - idx(foreign key) ----------ㅣ
- playerID(key) -ㅣ------ - playerID(foreign key)       ㅣ
- name           ㅣ                                     ㅣ
                 ㅣ       [Pitchers]                    ㅣ
                 ㅣ       - idx(foreign key) -----------ㅣ
                 ㅣ------ - playerID(foreign key)
```

# Columns

### PlayerID  
playerID = Column(Integer)   
name = Column(String(20))   

### Batters  
idx = Column(Integer)  
PlayerID = Column(Integer)    
position = Column(String(3))   
i_1 = Column(Integer)    
i_2 = Column(Integer)    
i_3 = Column(Integer)    
i_4 = Column(Integer)    
i_5 = Column(Integer)    
i_6 = Column(Integer)    
i_7 = Column(Integer)    
i_8 = Column(Integer)    
i_9 = Column(Integer)    
i_10 = Column(Integer)    
i_11 = Column(Integer)    
i_12 = Column(Integer)  
i_13 = Column(Integer)    
i_14 = Column(Integer)    
i_15 = Column(Integer)    
i_16 = Column(Integer)    
i_17 = Column(Integer)    
i_18 = Column(Integer)    
hit = Column(Integer)    
bat_num = Column(Integer)    
hit_prob = Column(Integer)    
hit_get = Column(Integer)    
own_get = Column(Integer)   

### Pitchers 
idx = Column(Integer)  
PlayerID = Column(Integer)    
position = Column(String(3))      
join = Column(Integer)  
inning = Column(Integer)  
rest = Column(Integer)  
result = Column(Integer)    
save = Column(Integer)    
hold = Column(Integer)    
strikeout = Column(Integer)    
deadball = Column(Integer)    
losescore = Column(Integer)    
earnedrun = Column(Integer)    
pitchnum = Column(Integer)    
hited = Column(Integer)    
homerun = Column(Integer)    
hitnum = Column(Integer)    
hitter = Column(Integer)    

### Scoreboards
idx = Column(Integer)  
TeamID = Column(Integer)     
result = Column(Integer)    
i_1 = Column(Integer)    
i_2 = Column(Integer)    
i_3 = Column(Integer)    
i_4 = Column(Integer)    
i_5 = Column(Integer)    
i_6 = Column(Integer)    
i_7 = Column(Integer)    
i_8 = Column(Integer)    
i_9 = Column(Integer)    
i_10 = Column(Integer)    
i_11 = Column(Integer)    
i_12 = Column(Integer)  
i_13 = Column(Integer)    
i_14 = Column(Integer)    
i_15 = Column(Integer)    
i_16 = Column(Integer)    
i_17 = Column(Integer)    
i_18 = Column(Integer)  
R = Column(Integer)    
H = Column(Integer)    
E = Column(Integer)    
B = Column(Integer)    
year = Column(Integer)   
month = Column(Integer)    
day = Column(Integer)   
week  = Column(Integer)     
home = Column(Integer)   
away = Column(Integer)   
dbheader = Column(Integer)   

