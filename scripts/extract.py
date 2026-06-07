import pandas as pd
import io

def extract_twitch_data():
    with open("data/raw/Twitch_game_data.csv", "r", encoding="cp1252", errors="ignore") as f:
        linhas = f.readlines()
    linhas_limpas = []
    for linha in linhas:
        linha = linha.strip()
        if linha.startswith('"') and linha.endswith('"'):
            linha = linha[1:-1] 
        linha = linha.replace('""', '"')
        linhas_limpas.append(linha)
    
    conteudo_csv = "\n".join(linhas_limpas)
    return pd.read_csv(io.StringIO(conteudo_csv), sep=',')

def extract_esports_data():
    with open("data/raw/HistoricalEsportData.csv", "r", encoding="cp1252", errors="ignore") as f:
        linhas = f.readlines() 
    linhas_limpas = []
    for linha in linhas:
        linha = linha.strip()
        if linha.startswith('"') and linha.endswith('"'):
            linha = linha[1:-1]
        linha = linha.replace('""', '"')
        linhas_limpas.append(linha)
    
    conteudo_csv = "\n".join(linhas_limpas)
    return pd.read_csv(io.StringIO(conteudo_csv), sep=',')
                        
def extract_games_data():
    return pd.read_csv("data/raw/Ultimate_Games_Dataset.csv", encoding="cp1252", encoding_errors="ignore")
                        
def extract_all():
    print("Extraindo dados brutos dos datasets.")
    twitch = extract_twitch_data()
    esports = extract_esports_data()
    games = extract_games_data()
    print("Dados extraidos com sucesso.")
    return twitch, esports, games