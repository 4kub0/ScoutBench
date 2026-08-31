import pandas as pd
df = pd.read_csv('data/processed/master_players.csv')
print('Players with # in name:', len(df[df['player'].str.contains('#')]))
print()
print('Real clubs:')
for club in ['Barcelona','Real Madrid','Manchester City','Arsenal','Liverpool','Bayern Munich','PSG','Inter Milan','Juventus','Napoli','Atletico Madrid','Chelsea','Tottenham','Bayer Leverkusen','Borussia Dortmund','Aston Villa','Monaco','Marseille']:
    c = df[df['team']==club]
    print(f'  {club}: {len(c)} players')
print()
print('Sample generated names (Sevilla):')
print(df[df['team']=='Sevilla']['player'].tolist())
print()
print('Sample generated names (Wolves):')
print(df[df['team']=='Wolves']['player'].tolist())
