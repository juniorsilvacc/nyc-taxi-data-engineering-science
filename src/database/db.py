import os
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import text

load_dotenv()

def get_engine():
    url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME")
    )
    
    engine = create_engine(url)
    
    max_retries = 5
    retry_interval = 5

    print(f"Tentando conectar ao banco em {os.getenv('DB_HOST')}...")

    for i in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Banco de dados pronto para receber conexões!")
            return engine
        except Exception as e:
            print(f"Banco ainda não disponível (Tentativa {i+1}/{max_retries}). Aguardando {retry_interval}s...")
            print(f"DEBUG: O erro real é: {e}")
            time.sleep(retry_interval)
            
    raise Exception("Erro: Não foi possível conectar ao banco de dados após várias tentativas.")