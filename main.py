from scripts.extract import extract_all
from scripts.transform import transform_all
from scripts.load import load_data

def run_pipeline():
    print("Iniciando pipeline de ETL")
    
    twitch, esports, games = extract_all()
    print("-" * 30)
    
    df_transformed = transform_all(twitch, esports, games)
    print("-" * 30)
    
    load_data(df_transformed)
    
    print("Pipeline executada com sucesso.")

if __name__ == "__main__":
    run_pipeline()