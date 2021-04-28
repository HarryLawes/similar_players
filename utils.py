import pandas as pd

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
    possession = possession[['90s','Succ%','#Pl','Carries','TotDist','PrgDist','01-Mar','CPA']]
    possession = possession.rename(columns={'01-Mar':'Final3rdDrib'})
    possession['#Pl'] = round(possession['#Pl']/possession['90s'],2)
    possession['Carries'] = round(possession['Carries']/possession['90s'],2)
    possession['Final3rdDrib'] = round(possession['Final3rdDrib']/possession['90s'],2)
    possession['CPA'] = round(possession['CPA']/possession['90s'],2)
    possession['PrgRatioDrib'] = round(possession['PrgDist']/possession['TotDist'],2)
    possession = possession.fillna(possession.median())
    possession = possession[['Succ%','#Pl','Carries','PrgRatioDrib','Final3rdDrib','CPA']]
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