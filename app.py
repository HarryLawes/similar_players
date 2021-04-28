import streamlit as st
import joblib
from model import find_similar_players

st.markdown("""
## Pick a player and we'll find you similar players
""")

player_name = st.text_input("Player Name")
season_input = st.selectbox("Season", ('2019/20', '2020/21'))
if season_input == '2019/20':
    season = 20
else:
    season = 21

number = int(st.number_input("Number of Players", max_value=20,value=5, step=1))

table = find_similar_players(player_name, season, n_players=number).set_index('Player')
info_table = table[['Nation','Pos','Age','Squad','Comp','Season']]

st.dataframe(info_table)

if info_table.head(1)['Pos'][player_name] == 'DF':
    stats = table[['Tkl','Tkl%','Past','Press','Press%','Blocks','Int','Clr','Err']]
if info_table.head(1)['Pos'][player_name] == 'DFMF':
    stats = table[['Short%','Mid%','Long%','Carries','Tkl%','Blocks','Int','Clr','Err']]

st.dataframe(stats)

st.text("Players listed in order of similarity")