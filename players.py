import streamlit as st
import pandas as pd
import joblib
from model import find_similar_players
from utils import draw_plot

def app():
    players = pd.read_csv('similar_players/data/players.csv')
    players = players.drop(columns=['Unnamed: 0'])

    st.markdown("""
    ## Pick a player and we'll find you similar players
    """)

    player_name = st.text_input("Player Name").title()
    season_input = st.selectbox("Season", ('2019/20', '2020/21'))
    if season_input == '2019/20':
        season = 2020
    else:
        season = 2021

    number = int(st.number_input("Number of Players", min_value=5,max_value=20,value=5, step=1))
    if player_name in players['Player'].unique():
        if st.checkbox('Include same player'):
            table = find_similar_players(player_name, season, n_players=number, return_same_player=True)
        else:
            table = find_similar_players(player_name, season, n_players=number)
        table_index = table.set_index('Player')
        info_table = table[['Nation','Pos','Age','Squad','Comp','Season']]

        st.dataframe(table_index)
        st.text("Players listed in order of similarity")

        position = players[players['Player'] == player_name]['Pos'].mode()[0]

        plot = draw_plot(player_name, season, position, table)
        st.write(plot)
        st.write("Definitions")
        if position == 'DF':
            st.text("CrsPA:     Crosses into the Penalty Area Per 90 Mins")
            st.text("xA:        Expected Assists Per 90 Mins")
            st.text("Err:       Errors Leading to Goals Per 90 Mins")
            st.text("Press:     Pressures Per 90 Mins")
            st.text("Tkl%:      Percentage of Dribblers Tackled")
            st.text("Int:       Number of Interceptions Per 90 Mins")
            st.text("Blocks:    Number of Passes and Shots Blocked Per 90 Mins")
            st.text("Prog:      Forward carries of over 5 metres (excl. those in defensive 3rd) Per 90 Mins")
        if position == 'DFMF':
            st.text("CrsPA:     Crosses into the Penalty Area Per 90 Mins")
            st.text("xA:        Expected Assists Per 90 Mins")
            st.text("PrgRatio:  Percentage of passing distance that is forward")
            st.text("Passes:    Passes Per 90 Mins")
            st.text("Prog:      Forward carries of over 5 metres (excl. those in defensive 3rd) Per 90 Mins")
            st.text("Int:       Number of Interceptions Per 90 Mins")
            st.text("Tkl%:      Percentage of Dribblers Tackled")
            st.text("Press:     Pressures Per 90 Mins")
        if position == 'MF':
            st.text("PrgRatio:      Percentage of passing distance that is forward")
            st.text("xA:            Expected Assists Per 90 Mins")
            st.text("Passes:        Passes Per 90 Mins")
            st.text("Prog:          Forward carries of over 5 metres (excl. those in defensive 3rd) Per 90 Mins")
            st.text("PrgRatioDrib:  Percentage of dribbling distance that is forward")
            st.text("Tkl:           Number of Tackles Attempted Per 90 Mins")
            st.text("Press:         Pressures Per 90 Mins")
            st.text("npxG:          Non-Penalty Expected Goals Per 90 Mins")
        if position == 'MFFW' or position == 'FWMF':
            st.text("npxG:          Non-Penalty Expected Goals Per 90 Mins")
            st.text("npxG/Sh:       Non-Penalty Expected Goals Per Shot")
            st.text("PrgRatio:      Percentage of Passing Distance that is Forward")
            st.text("KP:            Key Passes Per 90 Mins")
            st.text("xA:            Expected Assists Per 90 Mins")
            st.text("Prog:          Forward Carries of Over 5 Metres (excl. those in defensive 3rd) Per 90 Mins")
            st.text("Final3rdDrib:  Number of Dribbles into the Final 3rd Per 90 Mins")
            st.text("Press:         Pressures Per 90 Mins")
        if position == 'FW':
            st.text("npxG:      Non-Penalty Expected Goals Per 90 Mins")
            st.text("npxG/Sh:   Non-Penalty Expected Goals Per Shot")
            st.text("SoT%:      Shots on Target Percentage")
            st.text("Sh/90:     Shots Per 90 Mins")
            st.text("Passes:    Passes Per 90 Mins")
            st.text("xA:        Expected Assists Per 90 Mins")
            st.text("Prog:      Forward Carries of Over 5 Metres (excl. those in defensive 3rd) Per 90 Mins")
            st.text("Press:     Pressures Per 90 Mins")
        if position == 'DFFW' or position == 'FWDF':
            st.text("npxG:      Non-Penalty Expected Goals Per 90 Mins")
            st.text("xA:        Expected Assists Per 90 Mins")
            st.text("CrsPA:     Crosses into the Penalty Area Per 90 Mins")
            st.text("KP:        Key Passes Per 90 Mins")
            st.text("#Pl:       Number of Players Dribbled Past Per 90 Mins")
            st.text("Prog:      Forward Carries of Over 5 Metres (excl. those in defensive 3rd) Per 90 Mins")
            st.text("Tkl:       Number of Tackles Attempted Per 90 Mins")
            st.text("Press:     Pressures Per 90 Mins")
    else:
        st.warning("Please choose a valid player name. For a full list of players available,\
        look in the index")  

    if st.button('Click here to learn how this works!'):
        st.write("The similarity rankings are based on the output of a K-Nearest Neighbours\
        model. This is a model that calculates the distances between each player based on\
        all the different metrics in the interactive table above, which are all given equal\
        weighting. It can then rank the other players by distance and select the\
        'Nearest Neighbours' of the chosen player.")
        st.write("""The data comes from [FBRef](https://fbref.com/), and includes all
        players in Europe's top five leagues who have played at least five 90s
        in that season.""")