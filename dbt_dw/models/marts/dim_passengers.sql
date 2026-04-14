with dim_passengers as (
    select distinct passenger_count from {{ ref('stg_nyc_taxi') }}
)

select
    passenger_count as passenger_key,
    case 
        when passenger_count = 1 then 'Single Passenger'
        when passenger_count between 2 and 4 then 'Small Group'
        else 'Large Group/Van'
    end as passenger_capacity
from dim_passengers