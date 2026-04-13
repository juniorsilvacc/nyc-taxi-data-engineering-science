import sys
from src.database.db import get_engine
from src.jobs.extract_taxi import extract_taxi_csv_to_parquet
from src.jobs.transform_taxi_silver import transform_bronze_to_silver

def main():
    print(f"\n{'#'*60}")
    print(f"{'PIPELINE NYC TAXI - DATA ENGINEERING':^60}")
    print(f"{'#'*60}\n")

    try:
        # 1. HEALTH CHECK (Garante que o banco de dados no Docker está pronto antes de gastar CPU com Spark)
        print("Verificando disponibilidade do Banco de Dados...")
        get_engine()
        
        # 2. CAMADA BRONZE (Lê os CSVs brutos e converte para Parquet)
        print("\nExecutando extração para Camada Bronze...")
        extract_taxi_csv_to_parquet()
        
        # 3. CAMADA SILVER (Limpeza, Deduplicação, Feature Engineering e Carga no Postgres via JDBC)
        print("\nExecutando transformação para Camada Silver e Carga no PostgreSQL...")
        transform_bronze_to_silver()

    except Exception as e:
        print(f"Erro: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()