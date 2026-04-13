from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from src.database.postgres_to_load import load_silver_to_postgres
import os

def transform_bronze_to_silver():
    """
    Realiza a limpeza, padronização, pré-processamento e faz a carga no Postgres via JDBC.
    """
    
    base_path = os.getcwd()
    input_path = os.path.join(base_path, "data/bronze/nyc_taxi")
    output_path = os.path.join(base_path, "data/silver/nyc_taxi")
    
    spark = SparkSession.builder \
        .appName("NYC_Taxi_Silver_Transformation") \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "4g") \
        .config("spark.memory.offHeap.enabled", "true") \
        .config("spark.memory.offHeap.size", "2g") \
        .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2") \
        .config("spark.sql.shuffle.partitions", "200") \
        .getOrCreate()

    print(f"Lendo dados da Bronze em: {input_path}")

    try:
        df_bronze = spark.read.parquet(input_path)

        # 1. Padronização de nomes, Tipagem e Tratamento de Nulos...
        df_silver = df_bronze.select(
            F.col("VendorID").cast("int").alias("vendor_id"),
            F.to_timestamp(F.col("tpep_pickup_datetime"), "yyyy-MM-dd HH:mm:ss").alias("pickup_datetime"),
            F.to_timestamp(F.col("tpep_dropoff_datetime"), "yyyy-MM-dd HH:mm:ss").alias("dropoff_datetime"),
            F.coalesce(F.col("passenger_count").cast("int"), F.lit(1)).alias("passenger_count"), # Se nulo, assume 1
            F.col("trip_distance").cast("double").alias("trip_distance"),
            F.col("fare_amount").cast("double").alias("fare_amount"),
            F.col("tip_amount").cast("double").alias("tip_amount"),
            F.col("total_amount").cast("double").alias("total_amount")
        )
        
        # 2. Deduplicação
        initial_count = df_silver.count()
        df_silver = df_silver.dropDuplicates(["vendor_id", "pickup_datetime", "dropoff_datetime", "trip_distance"])
        
        after_dedup_count = df_silver.count()
        print(f"Deduplicação concluída. Registros duplicados removidos: {initial_count - after_dedup_count}")
        
        # 3. Limpeza de Anomalias (Data Quality)
        df_silver = df_silver.filter(
            (F.col("total_amount") > 0) & 
            (F.col("trip_distance") > 0) &
            (F.col("pickup_datetime").isNotNull()) &
            (F.col("dropoff_datetime") > F.col("pickup_datetime"))
        )
        
        # 4. Feature Engineering (Criação de Colunas de Tempo)
        df_silver = df_silver.withColumn("trip_duration_minutes", 
            (F.unix_timestamp("dropoff_datetime") - F.unix_timestamp("pickup_datetime")) / 60
        ).withColumn("hour_of_day", F.hour("pickup_datetime")) \
         .withColumn("day_of_week", F.dayofweek("pickup_datetime")) \
         .withColumn("is_weekend", F.when(F.col("day_of_week").isin(1, 7), True).otherwise(False))
        
        # 5. Auditoria
        final_count = df_silver.count()
        print(f"Limpeza de anomalias concluída. Registros removidos: {after_dedup_count - final_count}")
        print(f"Total de registros na Silver: {final_count:,}")

        # 6. Salvando na Silver com particionamento
        print(f"Gravando dados na Silver em: {output_path}")
        df_silver.repartition(100).write.mode("overwrite").parquet(output_path)
        
        # 7. Carga para o Banco de Dados (PostgreSQL)
        load_silver_to_postgres(df_silver)
        
        print("✅ Camada Silver concluída com sucesso!")

    except Exception as e:
        print(f"Erro na transformação Silver: {e}")
    finally:
        spark.stop()
