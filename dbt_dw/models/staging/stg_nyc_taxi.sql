with source as (
    select * from {{ source('dbt_dw', 'nyc_taxi_etl') }}
),

renamed as (
    select
        -- Identificadores
        vendor_id,
        rate_code_id,
        payment_type_id,
        
        -- Datas e Horas
        pickup_datetime,
        dropoff_datetime,
        hour_of_day,
        day_of_week,
        is_weekend,
        
        -- Métricas
        passenger_count,
        trip_distance,
        fare_amount,
        tip_amount,
        total_amount,
        trip_duration_minutes,
        
        -- Localização
        pickup_longitude,
        pickup_latitude,
        dropoff_longitude,
        dropoff_latitude,
        
        -- Auditoria
        current_timestamp as dbt_updated_at
    from source
)

select * from renamed