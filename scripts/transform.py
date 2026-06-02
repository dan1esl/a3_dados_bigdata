import pandas as pd

def transform_all(df_twitch, df_esports, df_games):
    print("Iniciando a padronização dos dados.")

    df_twitch.columns = df_twitch.columns.str.strip().str.replace('"', '').str.replace("'", "")
    df_esports.columns = df_esports.columns.str.strip().str.replace('"', '').str.replace("'", "")
    df_games.columns = df_games.columns.str.strip().str.replace('"', '').str.replace("'", "")

    df_esports['Game'] = df_esports['Game'].str.strip().str.lower()
    df_games['title'] = df_games['title'].str.strip().str.lower()
    df_twitch['Game'] = df_twitch['Game'].str.strip().str.lower()  

    df_esports['Date'] = pd.to_datetime(df_esports['Date'])
    df_esports['Year'] = df_esports['Date'].dt.year
    df_esports['Month'] = df_esports['Date'].dt.month

    df_twitch['Year'] = df_twitch['Year'].astype(int)
    df_twitch['Month'] = df_twitch['Month'].astype(int)
    df_esports['Year'] = df_esports['Year'].astype(int)
    df_esports['Month'] = df_esports['Month'].astype(int)

    print("Fazendo merge entre dados da Twitch e de Esports por jogo e data")
    df_twitch_esports = pd.merge(
        df_twitch,
        df_esports,
        on=['Game','Year','Month'],
        how='inner'
    )
    print("Padronização da coluna Game.")
    df_final = pd.merge(
        df_twitch_esports,
        df_games,
        left_on='Game',
        right_on='title',
        how='left'
    )
    if 'title' in df_final.columns:
        df_final = df_final.drop(columns=['title'])
    
    return df_final