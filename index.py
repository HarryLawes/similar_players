import streamlit as st
import pandas as pd

def app():
    st.title('All Players')
    players = pd.read_csv('similar_players/data/players.csv')
    players = players.drop(columns=['Unnamed: 0'])
    players = players[players['Pos'] != 'GK']

    player_table = players[['Player','Nation','Pos','Squad','Comp', 'Age']].groupby(['Player','Squad']).agg({
    'Nation':'max','Pos':'max','Comp':'max','Age':'max'}).reset_index()

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
        player_table = player_table[player_table['Pos'] == position]

    if st.checkbox('Filter by Nation'):
        country = st.selectbox("Nation",('Albania','Algeria','Angola','Argentina','Armenia','Australia',
        'Austria','Belgium','Benin','Bolivia','Bosnia and Herzegovina','Brazil','Bulgaria',
        'Burkina Faso','Cameroon','Canada','Cape Verde','Central African Republic','Chad',
        'Chile','China','Colombia','Costa Rica','Croatia','Cuba','Czech Republic','DR Congo',
        'Denmark','Dominica','Ecuador','Egypt','England','Equatorial Guinea','Estonia',
        'Faroe Islands','Finland','France','French Guyana','Gabon','Gambia','Georgia','Germany',
        'Ghana','Greece','Guadeloupe','Guinea','Guinea-Bissau','Honduras','Hungary','Iceland',
        'Iran','Ireland','Israel','Italy','Ivory Coast','Jamaica','Japan','Kenya','Kosovo',
        'Libya','Lithuania','Luxembourg','Madagascar','Mali','Martinique','Mauritania','Mexico',
        'Moldova','Montenegro','Morocco','Mozambique','Netherlands','New Caledonia','New Zealand',
        'Nigeria','North Macedonia','Northern Ireland','Norway','Panama','Paraguay','Peru',
        'Poland','Portugal','Republic of Congo','Reunion','Romania','Russia','Scotland','Senegal',
        'Serbia','Sierra Leone','Slovakia','Slovenia','South Africa','South Korea','Spain',
        'St Kitts and Nevis','Sweden','Switzerland','Tanzania','Togo','Tunisia','Turkey','USA',
        'Ukraine','Uruguay','Uzbekistan','Venezuela','Wales','Zambia','Zimbabwe'))
        nations = {'Ireland':'IRL', 'England':'ENG', 'Spain':'ESP', 'Scotland':'SCO',
        'Belgium':'BEL', 'Australia':'AUS', 'Wales':'WAL', 'Senegal':'SEN', 'Mauritania':'MTN',
        'Germany':'GER', 'France':'FRA', 'Mali':'MLI','Ivory Coast':'CIV', 'Guinea':'GUI',
        'Ghana':'GHA', 'Burkina Faso':'BFA', 'Morocco':'MAR', 'Montenegro':'MNE',
        'Algeria':'ALG','Hungary':'HUN','Switzerland':'SUI','Argentina':'ARG','Paraguay':'PAR',
        'Austria':'AUT', 'Jamaica':'JAM','Colombia':'COL','Portugal':'POR','Cameroon':'CMR',
        'Uruguay':'URU', 'Libya':'LBY','Egypt':'EGY','Turkey':'TUR','Togo':'TOG',
        'Brazil':'BRA','Italy':'ITA','Sweden':'SWE','Serbia':'SRB','North Macedonia':'MKD',
        'Russia':'RUS','Czech Republic':'CZE','Nigeria':'NGA','Norway':'NOR','Guinea-Bissau':'GNB',
        'Romania':'ROU','Chile':'CHI','Iceland':'ISL','USA':'USA','Iran':'IRN','Canada':'CAN',
        'Bosnia and Herzegovina':'BIH','Albania':'ALB', 'Kosovo':'KVX','Greece':'GRE',
        'Angola':'ANG','Denmark':'DEN','Croatia':'CRO','Mexico':'MEX','Bulgaria':'BUL',
        'Ukraine':'UKR','Ecuador':'ECU','Honduras':'HON','Netherlands':'NED','Equatorial Guinea':'EQG',
        'Poland':'POL', 'DR Congo':'COD', 'Moldova':'MDA','Sierra Leone':'SLE', 
        'Northern Ireland':'NIR', 'Tunisia':'TUN','South Africa':'RSA','Gabon':'GAB','Chad':'CHA',
        'Benin':'BEN','New Zealand':'NZL', 'Martinique':'MTQ','Peru':'PER','Japan':'JPN',
        'Venezuela':'VEN','Slovakia':'SVK', 'French Guyana':'GUF','Gambia':'GAM',
        'Lithuania':'LTU','Uzbekistan':'UZB','Finland':'FIN','Central African Republic':'CTA',
        'Georgia':'GEO','Estonia':'EST','Armenia':'ARM','South Korea':'KOR','Israel':'ISR',
        'Slovenia':'SVN','Bolivia':'BOL','Madagascar':'MAD','Faroe Islands':'FRO','Panama':'PAN',
        'Cape Verde':'CPV','Costa Rica':'CRC','Luxembourg':'LUX', 'Republic of Congo':'CGO',
        'Reunion':'REU', 'Dominica':'DOM','Zimbabwe':'ZIM','Tanzania':'TAN','Mozambique':'MOZ',
        'Guadeloupe':'GPE','Cuba':'CUB', 'St Kitts and Nevis':'SKN','Zambia':'ZAM',
        'Kenya':'KEN','New Caledonia':'NCL','China':'CHN'}
        selection = nations[country]
        player_table = player_table[player_table['Nation'] == selection]

    if st.checkbox('Filter by Team'):
        team_name = st.text_input("Team")
        selected_teams = []
        for team in list(players['Squad'].unique()):
            if team_name in team:
                selected_teams.append(team)
        if len(selected_teams) > 0:
            tables = []
            for team in selected_teams:
                new_table = player_table[player_table['Squad'] == team]
                tables.append(new_table)
            player_table = pd.concat(tables)
        else:
            st.warning('Your search has returned no players')

    if st.checkbox('Filter by League'):
        league = st.selectbox("League", ('Premier League','La Liga','Ligue 1','Serie A','Bundesliga'))
        player_table = player_table[player_table['Comp'] == league]
    
    st.write(player_table)
