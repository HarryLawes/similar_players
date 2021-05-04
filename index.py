import streamlit as st
import pandas as pd

def app():
    players = pd.read_csv('similar_players/data/players.csv')
    players = players.drop(columns=['Unnamed: 0'])

    player_table = players[['Player','Nation','Pos','Squad','Comp']].groupby(['Player']).agg(pd.Series.mode).reset_index()

    if st.checkbox('Filter by Name'):
        player_name = st.text_input("Player Name").title()
        #league = st.selectbox("League", ('Premier League','Ligue 1','Serie A','Bundesliga','La Liga'))
        selected_names = []
        for name in list(players['Player'].unique()):
            if player_name in name:
                selected_names.append(name)
        if len(selected_names) > 0:
            tables = []
            for name in selected_names:
                new_table = player_table[player_table['Player']== name]
                tables.append(new_table)
            player_table = pd.concat(tables)
        else:
            st.warning('Your search has returned no players. Make sure names are capitalised')

    if st.checkbox('Filter by Position'):
        position = st.selectbox("Position", ('DF', 'DFFW', 'FWDF','DFMF','MF','MFFW','FWMF','FW'))
        player_table = player_table[player_table['Pos'] == str(position)]

    if st.checkbox('Filter by Team'):
        team_name = st.text_input("Team")
        selected_teams = []
        for team in list(players['Squad'].unique()):
            if team_name in team:
                selected_teams.append(team)
        if len(selected_teams) > 0:
            tables = []
            for team in selected_teams:
                new_table = player_table[(player_table['Squad'] == team) | (player_table['Squad'].count(team) > 0)]
                tables.append(new_table)
            player_table = pd.concat(tables)
        else:
            st.warning('Your search has returned no players')
    
    st.write(player_table)
