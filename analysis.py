#analysis

#Libraries -------------------------------------------------------------------
import pandas as pd
from sklearn.feature_selection import mutual_info_regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
#from sklearn.linear_model import Ridge
#from sklearn.linear_model import ElasticNet
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
# ----------------------------------------------------------------------------

#Data Prep -------------------------------------------------------------------
df1 = pd.read_csv('data_more.csv')                                             #read in data set
df2 = df1.dropna()                                                             #remove null values
#remove columns with non number values, and other non-relevant values like year, height, and weight
df3 = df2.drop(columns = ['yearID', 'teamID', 'lgID', 'playerID', 'playerName', 'OPS_avg',
                          'birthCountry', 'birthCity', 'bats', 'throws', 'debut', 'birthYear', 'height','weight']) 


df3.loc[df3['WAR30']<0, 'WAR30'] = 0                                           #replace -WAR30 with 0 per Assumption 4
df3.loc[df3['WAR']<0, 'WAR'] = 0                                               #replace -WAR with 0 per Assumption 4
#-----------------------------------------------------------------------------

#Feature selection -----------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(df3.drop(columns = 'WAR30'), df3['WAR30'],
                                                    test_size = .2,
                                                    random_state = 0)          #split the model into a train and test set 80/20
mutual_info = mutual_info_regression(X_train, y_train, n_neighbors = 20)       #gets the correlation between each feature and the target variable
mutual_info = pd.Series(mutual_info)                                           #turns features into a series
mutual_info.index = X_train.columns                                            #sets index by column name
mutual_info.sort_values(ascending = False, inplace=True)                       #sort by decreasing correlation
features_for_model = mutual_info.head(n=20)                                    #top20 relevant features
#-----------------------------------------------------------------------------

#Regression Model ------------------------------------------------------------
df4 = pd.concat([df3[features_for_model.index], df3.WAR30], axis = 1)          #dataframe with top features and target variable WAR30
X_train, X_test, y_train, y_test = train_test_split(df4.drop(columns = 'WAR30'), df4['WAR30'],
                                                    test_size = .2,
                                                    random_state = 0)          #split the model into a train and test set 80/20
linreg = LinearRegression()                                                    #declare the model
linreg.fit(X_train, y_train)                                                   #fit the train set to the test set
linreg_y_pred = linreg.predict(X_test)                                         #predict the WAR30 for the test set
linreg_score = r2_score(y_test, linreg_y_pred)                                 #compare predictions to actual
print('LinReg Score:  '+ str(linreg_score))                                    #print the score r2=.542
#-----------------------------------------------------------------------------

#Summarize Results -----------------------------------------------------------
player_sum = pd.DataFrame(y_test)                                              #dataframe with target test data                                         
player_sum.insert(1, 'WAR30_pred', linreg_y_pred)                              #add model prediction
player_sum.insert(0, 'Name', df2.loc[player_sum.index].playerName)             #add player name
player_sum.insert(1, 'Year', df2.loc[player_sum.index].yearID)                 #add year 
player_sum.insert(2, 'Age', df2.loc[player_sum.index].playerAge)               #add player age
player_sum.insert(3, 'Error', player_sum.WAR30-player_sum.WAR30_pred)          #error between predicted and actual
player_sum.insert(4, '%Error', abs(player_sum.Error/player_sum.WAR30*100))     #percent error
player_sum = pd.concat([player_sum, X_test], axis = 1)                         #add test data inputs
player_sum.sort_values('%Error', inplace = True)                               #sort be decreasing error
player_sum = round(player_sum, 3)                                              #round values to 3rd decimal
# ----------------------------------------------------------------------------

#Plot Results ----------------------------------------------------------------
plt.scatter(player_sum.WAR, player_sum['%Error'])                              #plot season WAR by predicted %Error
plt.xlabel('Single Season WAR')                                                #x axis label
plt.ylabel('Percent Error in WAR prediction')                                  #y axis label
plt.title('Determining where the model Works Best')                            #title
#-----------------------------------------------------------------------------

#Sample to Evaluate ----------------------------------------------------------
recent = player_sum[player_sum.Year == 2017]                                   #players in the year 2017
recent = recent[recent.Age == 27]                                              #that were 27, turned 30 in 2021
recent.sort_values('Error', inplace = True)                                    #sort by decreasing Error
# ----------------------------------------------------------------------------


#Other Attempted Models ------------------------------------------------------
# =============================================================================
# rreg = Ridge(alpha = .05, normalize = True)
# rreg.fit(X_train, y_train)
# rreg_y_pred = rreg.predict(X_test)
# rreg_score = r2_score(y_test, rreg_y_pred)                                     #compare predictions to actual
# print('RReg Score:  '+ str(rreg_score))                                        #print the score=.512
# =============================================================================

# =============================================================================
# enreg = ElasticNet(alpha = 1, l1_ratio = .5, normalize = False)
# enreg.fit(X_train, y_train)
# enreg_y_pred = enreg.predict(X_test)
# enreg_score = r2_score(y_test, enreg_y_pred)                                   #compare predictions to actual
# print('ENReg Score:  '+ str(enreg_score))                                      #print the score=.507
# =============================================================================