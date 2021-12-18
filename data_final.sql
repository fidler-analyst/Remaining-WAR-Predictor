USE war_predict;

SELECT a.yearID, a.teamID, a.lgID, a.playerID, 
CONCAT(p.nameFirst,' ', p.nameLast) AS playerName,                    -- assembles player name
(b.yearID - p.birthYear) AS playerAge,                                -- determines player age
(AB+BB+IBB+HBP+SH+SF) AS 'PA',                                        -- total plate appearances
ROUND((H/AB),3) AS 'AVG',                                             -- batting average
ROUND((H+BB+IBB+HBP)/(AB+BB+IBB+HBP+SH+SF), 3) AS 'OBA',              -- on base percentage
ROUND(((H-2B-3B-HR) + 2*2B + 3*3B + 4*HR)/AB, 3) AS 'SLG',            -- slugging percentage
ROUND(SO/(AB+BB+IBB+HBP+SH+SF),3) AS 'K%',                            -- strike out rate
ROUND((BB/(AB+BB+IBB+HBP+SH+SF)),3) AS 'BB%',                         -- walk rate
ROUND((H-HR)/(AB-HR-SO+SF),3) AS 'BABIP',                             -- batting average on balls in play
ROUND(((H-2B-3B-HR) + 2*2B + 3*3B + 4*HR)*(H+BB)/(AB+BB),3) AS RC,    -- runs created

-- RAA_def defensive Runs Above Average
(ROUND(a.GS*(a.G_c*9+ a.G_1b*(-9.5) + a.G_2b*3 + a.G_3b*2 + a.G_ss*7 + a.G_lf*(-7) + a.G_cf*2.5 + a.G_rf*(-7) + a.G_dh*(-15))/150 
/(a.G_c+a.G_1b+a.G_2b+a.G_3b+a.G_ss+a.G_lf+a.G_rf+a.G_cf+a.G_dh),3)) AS RAA_def,
GS,
G, AB, R, H, 2B, 3B, HR, RBI, SB, CS, BB, SO, IBB, HBP, SH, SF, GIDP,    -- other offensive statistics in appearances table
birthYear, birthCountry, birthCity, weight, height, bats, throws, debut  -- other player information

FROM appearances a, batting b, people p                               -- tables used
WHERE a.playerID = b.playerID AND b.playerID = p.playerID             -- join by player id
AND a.yearID = b.yearID AND a.yearID >= 1994                          -- also join by year
AND G_p < 10 AND AB > 50                                              -- more than 50 AB's and less than 10 games pitching to remove pitchers
HAVING playerAge <= 30                                                -- players aged 30 or less
ORDER BY a.yearID,  a.playerID                                        -- order by year by player
