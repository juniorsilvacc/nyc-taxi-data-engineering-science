with source as (
    select * from {{ source('dbt_dw', 'nyc_taxi_etl') }}
),

renamed as (
    select
        vendor_id,
        pickup_datetime,
        dropoff_datetime,
        passenger_count,
        trip_distance,
        fare_amount,
        tip_amount,
        total_amount,
        trip_duration_minutes,
        hour_of_day,
        day_of_week,
        is_weekend,
        current_timestamp as dbt_updated_at
    from source
)

select * from renamed