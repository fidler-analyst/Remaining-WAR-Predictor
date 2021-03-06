#further data assembly
import pandas as pd

ranking = pd.read_csv('prospect_ranking.csv')                                  #read in prospect ranking
data = pd.read_csv('data.csv')                                                 #read in data.csv, result of data_final.sql script
data.insert(10, 'OPS', data.OBA + data.SLG)                                    #add OPS columns = OBA+SLG


#add OPS average -------------------------------------------------------------
data.insert(11, 'OPS_avg', [0]*len(data))                                      #blank column for yearly average OPS
AL = data[data.lgID == 'AL']                                                   #just american league
years = AL.yearID.drop_duplicates().to_list()                                  #list of years

for year in years:                                                             #iterate through years
    AL_year = AL[AL.yearID == year]                                            #dataframe of AL by year
    OPS_avg = round(AL_year.OPS.mean(),3)                                      #average OPS for the AL in that year
      
    data.loc[data['yearID'] == year, 'OPS_avg'] = OPS_avg                      #insert the annual league OPS average to dataframe
#-----------------------------------------------------------------------------


#RAA_off, RAA, WAR by year ---------------------------------------------------
data.insert(17, 'RAA_off', round(data.PA*(data.OPS-data.OPS_avg)/3.2135,3))    #calcs and inserts RAA_off to data
data.insert(18, 'RAA', data.RAA_off+data.RAA_def + 20)                         #calcs and inserts RAA to data
data.insert(19, 'WAR', data.RAA/10)                                            #calcs and inserts WAR to data
#-----------------------------------------------------------------------------


#add WAR achieved by each player through age 30 ------------------------------
data.insert(20, 'WAR30', [0]*len(data))                                        #blank column for cummulative war through age 30
players = data.playerID.drop_duplicates().to_list()                            #list of players

for player in players:                                                         #iterate through players
    player_df = data[data.playerID == player]                                  #dataframe of just the player
    WAR30 = sum(player_df.WAR)                                                 #total WAR generated by player from start through age 30
    data.loc[(data.playerID == player), 'WAR30'] = WAR30                       #insert cummulative WAR to dataframe for each player
#-----------------------------------------------------------------------------


#add debut age ---------------------------------------------------------------
data.insert(6, 'debutAge', data.debut.str[0:4].astype(int) - data.birthYear)   #inserts age player was at debut to data
#-----------------------------------------------------------------------------


#add prospect ranking --------------------------------------------------------
data.insert(7, 'rank', [250]*len(data))                                        #inserts a ranking of 250 for all players
                                                                               #since actual scale is 1-100, being unranked will
                                                                               #now assume that the player is average of 250
                                                                               #to prevent the model from being confused

r_players = ranking.lahman_id.drop_duplicates().to_list()                      #list of ranked players
for player in r_players:                                                       #iterate through ranked players
    r_player_df = ranking[ranking.lahman_id == player]                         #ranked player dataframe
    r_years = r_player_df.year.drop_duplicates().to_list()                     #list of years player was ranked
    
    for r_year in r_years:                                                     #iterate through ranked years
        r_df = r_player_df[r_player_df.year == r_year]                         #dataframe of ranked player for a single year   
        data.loc[(data.playerID == player) & (data.yearID == r_year), 
                 'rank'] = max(r_df.prospect_rank)                             #inserts ranking to data 
        

data.to_csv('data_more.csv', index = False)                                    #outputs resulting data set to csv