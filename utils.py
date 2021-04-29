import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge

players = pd.read_csv('similar_players/data/players.csv')
players = players.drop(columns=['Unnamed: 0'])
mod_players = players[players['90s']>5]

def clean_name(x):
    name = x.split('\\')[1]
    name = name.replace('-',' ')
    return name

def clean_country(x):
    new_string = ''
    for letter in x:
        if letter.upper() == letter and letter != ' ':
            new_string += letter
    return new_string

def clean_columns(df):
    df['Player'] = df['Player'].apply(clean_name)
    df['Nation'] = df['Nation'].apply(clean_country)
    df['Pos'] = df['Pos'].apply(lambda x: 'GK' if x == 'GKMF' else x)
    df['Comp'] = df['Comp'].apply(lambda x: x.replace(x.split(' ')[0] + ' ', ''))
    if df['Age'].dtype != 'int64':
        df['Age'] = df['Age'].apply(lambda x: int(x.split('-')[0]))
    df = df.drop(columns=['Rk','Born','MP','Starts','Min','Gls','Ast','G-PK','PK','PKatt','Gls.1','G+A','G+A-PK','xG','npxG',
                                'xA','npxG+xA','xG.1','xG+xA','npxG+xA.1','Matches'])
    df = df.rename(columns={'Ast.1':'Ast','G-PK.1':'npG','xA.1':'xA','npxG.1':'npxG'})
    return df

def missing_values(df):
    team_map = {'Saint-�tienne':'Saint-Etienne', 'C�diz':'Cadiz','Alav�s':'Alaves','N�mes':'Nimes',
            'K�ln':'Koln','Atl�tico Madrid':'Atletico Madrid','Legan�s':'Leganes','D�sseldorf':'Dusseldorf'}
    df['Squad'] = df['Squad'].map(team_map).fillna(df['Squad'])
    df['CrdY'] = round(df['CrdY']/df['90s'],2)
    df['CrdR'] = round(df['CrdR']/df['90s'],2)
    df = df.fillna(df.median())
    return df

def add_passing(df, season):
    passing = pd.read_csv(f'data/passing{season}.csv')
    passing.rename(columns={'Cmp.1':'ShortCmp','Att.1':'ShortAtt','Cmp%.1':'ShortComp%',
                        'Cmp.2':'MidCmp','Att.2':'MidAtt','Cmp%.2':'MidComp%',
                        'Cmp.3':'LongCmp','Att.3':'LongAtt','Cmp%.3':'LongComp%', '01-Mar':'Final3rd'}, inplace=True)
    passing['Short%'] = round(passing['ShortCmp']/passing['Cmp'],2)
    passing['Mid%'] = round(passing['MidCmp']/passing['Cmp'],2)
    passing['Long%'] = round(passing['LongCmp']/passing['Cmp'],2)
    passing['PrgRatio'] = round(passing['PrgDist']/passing['TotDist'],2)
    passing['Passes'] = round(passing['Att']/passing['90s'],2)
    passing['KP'] = round(passing['KP']/passing['90s'],2)
    passing['Final3rd'] = round(passing['Final3rd']/passing['90s'],2)
    passing['PPA'] = round(passing['PPA']/passing['90s'],2)
    passing['CrsPA'] = round(passing['CrsPA']/passing['90s'],2)
    passing = passing[['Passes','PrgRatio','Short%','Mid%','Long%','ShortComp%','MidComp%','LongComp%','KP','Final3rd','PPA','CrsPA']]
    passing = passing.fillna(passing.median())
    df = df.merge(passing, left_index=True, right_index=True)
    return df

def add_shooting(df, season):
    shooting = pd.read_csv(f'data/shooting{season}.csv')
    shooting = shooting[['SoT%','Sh/90','G/SoT','Dist','npxG/Sh']]
    shooting = shooting.fillna(0)
    df = df.merge(shooting, left_index=True, right_index=True)
    return df

def add_possession(df, season):
    possession = pd.read_csv(f'data/possession{season}.csv')
    possession = possession[['90s','Succ%','#Pl','Prog','TotDist','PrgDist','01-Mar','CPA']]
    possession = possession.rename(columns={'01-Mar':'Final3rdDrib'})
    possession['#Pl'] = round(possession['#Pl']/possession['90s'],2)
    possession['Prog'] = round(possession['Prog']/possession['90s'],2)
    possession['Final3rdDrib'] = round(possession['Final3rdDrib']/possession['90s'],2)
    possession['CPA'] = round(possession['CPA']/possession['90s'],2)
    possession['PrgRatioDrib'] = round(possession['PrgDist']/possession['TotDist'],2)
    possession = possession.fillna(possession.median())
    possession = possession[['Succ%','#Pl','Prog','PrgRatioDrib','Final3rdDrib','CPA']]
    df = df.merge(possession, left_index=True,right_index=True)
    return df

def add_defensive(df, season):
    defensive = pd.read_csv(f'data/defensive{season}.csv')
    defensive = defensive[['90s','Tkl','Tkl%','Past','Press','%','Sh','Int','Clr','Err']]
    defensive = defensive.rename(columns={'%':'Press%','Sh':'Blocks'})
    defensive['Tkl'] = round(defensive['Tkl']/defensive['90s'],2)
    defensive['Past'] = round(defensive['Past']/defensive['90s'],2)
    defensive['Press'] = round(defensive['Press']/defensive['90s'],2)
    defensive['Blocks'] = round(defensive['Blocks']/defensive['90s'],2)
    defensive['Int'] = round(defensive['Int']/defensive['90s'],2)
    defensive['Clr'] = round(defensive['Clr']/defensive['90s'],2)
    defensive['Err'] = round(defensive['Err']/defensive['90s'],2)
    defensive = defensive.fillna(defensive.median())
    defensive = defensive.drop(columns=['90s'])
    df = df.merge(defensive, left_index=True, right_index=True)
    return df

def get_season(year):
    players = pd.read_csv(f'data/general{year}.csv')
    players['Season'] = f'20{year}'
    players.insert(5, 'Season', players.pop('Season'))
    players = clean_columns(players)
    players = missing_values(players)
    players = add_passing(players,season = year)
    players = add_shooting(players,season = year)
    players = add_possession(players,season = year)
    players = add_defensive(players,season = year)
    return players

def draw_plot(player, season, template, table):
    mffw_cols = ['npxG','npxG/Sh','PrgRatio','KP','xA','Prog','Final3rdDrib','Press']
    mffw_colors = ['red','red','blue','blue','blue','yellow','yellow','green']
    fw_cols = ['npxG','npxG/Sh','SoT%','Sh/90','Passes','xA','Prog','Press']
    fw_colors = ['red','red','red','red','blue','blue','yellow','green']
    mf_cols = ['npxG','xA','PrgRatio','Passes','Prog','PrgRatioDrib','Tkl','Press']
    mf_colors = ['red','blue','blue','blue','yellow','yellow','green','green']
    df_cols = ['xA','CrsPA','Prog','Blocks','Int','Tkl%','Press','Err']
    df_colors = ['blue','blue','yellow','green','green','green','green','green']
    dfmf_cols = ['xA','CrsPA','PrgRatio','Passes','Prog','Int','Tkl%','Press']
    dfmf_colors = ['blue','blue','blue','blue','yellow','green','green','green']
    dffw_cols = ['npxG','xA','CrsPA','KP','#Pl','Prog','Tkl','Press']
    dffw_colors = ['red','blue','blue','blue','yellow','yellow','green','green']
    if template == 'FW':
        cols = fw_cols
        colors = fw_colors
    elif template == 'MFFW' or template == 'FWMF':
        cols = mffw_cols
        colors = mffw_colors
    elif template == 'MF':
        cols = mf_cols
        colors = mf_colors
    elif template == 'DF':
        cols = df_cols
        colors = df_colors
    elif template == 'DFMF':
        cols = dfmf_cols
        colors = dfmf_colors
    elif template == 'DFFW' or template == 'FWDF':
        cols = dffw_cols
        colors = dffw_colors
    label_coords = [(0.9,0.65),(0.65,0.9),(0.30,0.9),(0.01,0.65),(0.01,0.35),(0.30,0.075),(0.65,0.075),(0.9,0.35)]
    fig, axes = plt.subplots(2,3,figsize=(30,20))
    for i in range(2):
        for j in range(3):
            if i == 0:
                player = table['Player'][table.index[j]]
                season = table['Season'][table.index[j]]
            else:
                player = table['Player'][table.index[j+3]]
                season = table['Season'][table.index[j+3]]
            player_stats = players[(players['Player'] == player) & (players['Season']==season)]
            player_stats = player_stats[cols]
            maxs = mod_players[cols].max()
            player_viz = []
            for col in cols:
                player_viz.append(player_stats[col][player_stats.index[0]]/maxs[col])
            for n in range(8):
                axes[i,j].add_patch(Wedge((0.5,0.5),player_viz[n]*0.4,45*n,45*(n+1),edgecolor='black',facecolor=colors[n]))
                axes[i,j].annotate(cols[n],label_coords[n], fontsize=16)
                draw_circle = plt.Circle((0.5,0.5),0.4, fill=False)
                axes[i,j].add_artist(draw_circle)
                axes[i,j].axis('off')
                axes[i,j].set_title(f'{player}, {season-1}/{season-2000}', fontsize=24)
    plt.show()
    return fig