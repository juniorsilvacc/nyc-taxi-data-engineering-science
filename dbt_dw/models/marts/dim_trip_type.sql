with dim_trip_type as (
    select * from {{ ref('stg_nyc_taxi') }}
)

select
    case 
        when trip_distance <= 2 then 'Short Trip'
        when trip_distance > 2 and trip_distance <= 10 then 'Medium Trip'
        else 'Long Trip'
    end as trip_type_key,
    count(*) as total_occurrences
from dim_trip_type group by 1 