import sys
import pandas as pd
from utils import get_season
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

players = get_season(21)
players20 = get_season(20)
players = pd.concat([players, players20])

mod_players = players[players['90s']>5]
mod_players = mod_players.reset_index(drop=True)

X = mod_players.drop(columns=['Player','Nation','Pos','Squad','Comp', 'Season'])
y = mod_players['Age']

scaler = MinMaxScaler()
X_transformed=scaler.fit_transform(X)

knn = KNeighborsRegressor()
knn.fit(X_transformed,y)

player_name = sys.argv[1] + ' ' + sys.argv[2]
season = sys.argv[3]

def find_similar_players(player_name, season, n_players=5, return_same_player=False):
    index = mod_players[(mod_players['Player'] == player_name)\
                        &(mod_players['Season'] == f'20{season}')].index[0]
    distances, indices = knn.kneighbors(X_transformed[index:index+1], n_neighbors=n_players+2)
    similar_players = mod_players.iloc[indices[0], :]
    if return_same_player == False:
        similar_players = similar_players[(similar_players['Player']!=player_name)\
                                          |(similar_players['Season']==f'20{season}')]
    return similar_players.head(6)

print(find_similar_players(player_name, season))