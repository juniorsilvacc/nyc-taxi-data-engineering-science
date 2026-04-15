with dates as (
    select distinct pickup_datetime::date as date_day from {{ ref('stg_nyc_taxi') }}
)

select
    date_day as date_key,
    extract(year from date_day) as year,
    extract(month from date_day) as month,
    to_char(date_day, 'Day') as day_name,
    case 
        when extract(dow from date_day) in (0, 6) then 1 
        else 0 
    end as is_weekend
from dates