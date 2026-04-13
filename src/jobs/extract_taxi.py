from pyspark.sql import SparkSession
import os

def extract_taxi_csv_to_parquet():
    """
    Lê arquivos CSV de forma recursiva em data/raw e os salva como Parquet em data/bronze.
    """
    
    base_path = os.getcwd()
    input_path = os.path.join(base_path, "data/raw")
    output_path = os.path.join(base_path, "data/bronze/nyc_taxi")
        
    spark = SparkSession.builder \
        .appName("NYC_Taxi_Bronze_Ingestion") \
        .config("spark.executor.memory", "4g") \
        .config("spark.driver.memory", "4g") \
        .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2") \
        .getOrCreate()

    print(f"\n{'='*50}")
    print(f"INICIANDO EXTRAÇÃO BRONZE")
    print(f"Lendo de: {input_path}")
    print(f"Gravando em: {output_path}")
    print(f"{'='*50}\n")
    
    try:
        df_raw = spark.read.format("csv") \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .option("recursiveFileLookup", "true") \
            .option("pathGlobFilter", "*.csv") \
            .load(input_path)

        print("Calculando volume de registros (isso pode levar alguns minutos)...")
        total_rows = df_raw.count()
        print(f"✅ Sucesso! {total_rows:,} registros encontrados.")

        print("Convertendo e salvando em Parquet na camada Bronze...")
        
        # Salvando em Parquet
        #df_raw.write.mode("overwrite").parquet(output_path)
        df_raw.repartition(50).write.mode("overwrite").parquet(output_path)
        
        print(f"\n✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        print(f"Os dados estão prontos na pasta: {output_path}")

    except Exception as e:
        print(f"\nERRO DURANTE O PROCESSAMENTO:")
        print(str(e))
    finally:
        spark.stop()
