
# Tables
### PlayerID  
PlayerID = Column(Integer)   
name = Column(String(20))   

### TeamID  
TeamID = Column(Integer)    
name = Column(String(5))   

### Batters  
PlayerID   
position   
TeamID   
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
PlayerID   
position   
TeamID   
join   
inning   
rest   
win   
lose   
draw   
save   
hold   
strikeout   
deadball   
losescore   
earnedrun   
pitchnum   
hited   
homerun   
hitnum   
hitter   

### Scoreboards
TeamID   
result   
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
R   
H   
E   
B   
year   
month   
day   
week   
home   
away   
dbheader   
