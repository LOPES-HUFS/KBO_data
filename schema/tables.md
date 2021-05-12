
# Tables schema

```bash
[TeamID]                  [Scoreboards]
- teamID(key) ㅡㅡㅡㅡㅡ - TeamID(foreign key)
- name          
                            
                       
[PlayerID]                [Batters]
- playerID(key)ㅡㅣㅡㅡㅡ - playerID(foreign key)
- name           ㅣ
                 ㅣ        [Pitchers]
                 ㅣㅡㅡㅡ - playerID(foreign key)
```

# Columns

### PlayerID  
playerID = Column(Integer)   
name = Column(String(20))   

### TeamID  
teamID = Column(Integer)    
name = Column(String(5))   

### Batters  
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
hit = Column(Integer)    
bat_num = Column(Integer)    
hit_prob = Column(Integer)    
hit_get = Column(Integer)    
own_get = Column(Integer)   

### Pitchers 
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

