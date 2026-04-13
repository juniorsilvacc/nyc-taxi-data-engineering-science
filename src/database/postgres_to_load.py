import os

def load_silver_to_postgres(df_spark):
    """
    Realiza a carga total (Full Load) da camada Silver para o PostgreSQL via Spark JDBC.
    """
    
    db_host = os.getenv("DB_HOST", "db")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    
    db_url = f"jdbc:postgresql://{db_host}:5432/{db_name}"
    
    db_properties = {
        "user": db_user,
        "password": db_pass,
        "driver": "org.postgresql.Driver",
        "batchsize": "100000",
        "rewriteBatchedInserts": "true"
    }

    print(f"\n🚀 Iniciando carga no PostgreSQL: {db_url}")
    
    try:
        df_spark.repartition(10).write.jdbc(
            url=db_url, 
            table="nyc_taxi_etl", 
            mode="overwrite", 
            properties=db_properties
        )
        print("✅ Dados carregados com sucesso na tabela 'nyc_taxi_etl'!")
        
    except Exception as e:
        print(f"Erro ao carregar dados no Postgres: {e}")