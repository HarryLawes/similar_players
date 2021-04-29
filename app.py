import streamlit as st
import pandas as pd
import joblib
from model import find_similar_players
from utils import draw_plot

st.markdown("""
## Pick a player and we'll find you similar players
""")

player_name = st.text_input("Player Name")
season_input = st.selectbox("Season", ('2019/20', '2020/21'))
if season_input == '2019/20':
    season = 2020
else:
    season = 2021

number = int(st.number_input("Number of Players", min_value=5,max_value=20,value=5, step=1))

table = find_similar_players(player_name, season, n_players=number)
table_index = table.set_index('Player')
info_table = table[['Nation','Pos','Age','Squad','Comp','Season']]

st.dataframe(table_index)
st.text("Players listed in order of similarity")

players = pd.read_csv('similar_players/data/players.csv')
players = players.drop(columns=['Unnamed: 0'])
position = players[players['Player'] == player_name]['Pos'].mode()[0]

plot = draw_plot(player_name, season, position, table)
st.write(plot)

st.write("Definitions")
if position == 'DF':
    st.write("**CrsPA**: Crosses into the Penalty Area Per 90 Mins")
    st.write("**xA**: Expected Assists ")
    st.write("**Err**: Errors Leading to Goals Per 90 Mins")
    st.write("**Press**: Pressures Per 90 Mins")
    st.write("**Tkl%**: Percentage of Dribblers Tackled")
    st.write("**Int**: Number of Interceptions")
    st.write("**Blocks**: Number of Passes and Shots Blocked")
    st.write("**Prog**: Forward carries of over 5 metres (excl. those in defensive 3rd)")
if position == 'MF':
    st.write("**PrgRatio**: Percentage of passing distance that is forward")
    st.write("**xA**: Expected Assists Per 90 Mins")
    st.write("**Passes**: Passes Per 90 Mins")
    st.write("**Prog**: Forward carries of over 5 metres (excl. those in defensive 3rd)")
    st.write("**PrgRatioDrib**: Percentage of dribbling distance that is forward")
    st.write("**Tkl**: Number of Tackles Attempted Per 90 Mins")
    st.write("**Press**: Pressures Per 90 Mins")
    st.write("**npxG**: Non-Penalty Expected Goals Per 90 Mins")

