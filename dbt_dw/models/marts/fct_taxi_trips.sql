with fct_taxi_trips as (
    select * from {{ ref('stg_nyc_taxi') }}
)

select
    -- Chaves das Dimensões
    vendor_id as vendor_key,
    rate_code_id as rate_code_key,
    payment_type_id as payment_key,
    pickup_datetime::date as date_key,
    hour_of_day as time_key,
    passenger_count as passenger_key,

    -- Métricas
    trip_distance,
    fare_amount,
    tip_amount,
    total_amount,
    trip_duration_minutes,

    -- Localizações
    pickup_latitude,
    pickup_longitude,
    dropoff_latitude,
    dropoff_longitude
from fct_taxi_trips