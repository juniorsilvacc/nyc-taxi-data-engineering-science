with raw_location as (
    SELECT * FROM {{ ref('taxi_zone_lookup') }}
)

select
    cast(location_id as int) as location_key,
    borough,
    zone as zone_name,
    service_zone
from raw_location