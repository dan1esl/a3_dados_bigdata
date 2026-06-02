import os

def load_data(df_final):
    print("Carregando os dados na pasta gold")

    output_path = "data/gold/dados_unificados_esports.csv"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df_final.to_csv(output_path, index=False, encoding='utf-8')

    print("Dados carregados com sucesso.")