/*년도별 특정 팀의 경기 날짜 리스트*/
SELECT TeamID.teamname,
        scoreboards.year,
        scoreboards.month,
        scoreboards.day
from TeamID
    INNER JOIN scoreboards
on TeamID.teamid = scoreboards.teamid
where TeamID.teamname = 'HH';

/*년도별 특정 선수 HIT 개수*/
SELECT PlayerID.playername,
        scoreboards.year,
        batters.hit
from PlayerID
    INNER JOIN batters
    on PlayerID.playerid = batters.playerid
    INNER JOIN scoreboards
    on batters.idx = scoreboards.idx
where PlayerID.playername = 'RHJ';
