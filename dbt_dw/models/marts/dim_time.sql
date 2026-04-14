with dim_time as (
    select distinct hour_of_day from {{ ref('stg_nyc_taxi') }}
)

select
    hour_of_day as time_key,
    case 
        when hour_of_day between 0 and 5 then 'Madrugada'
        when hour_of_day between 6 and 11 then 'Manhã'
        when hour_of_day between 12 and 17 then 'Tarde'
        else 'Noite'
    end as shift_name,
    case 
        when hour_of_day in (7, 8, 9, 17, 18, 19) then 'Rush Hour'
        else 'Normal'
    end as traffic_condition
from dim_time