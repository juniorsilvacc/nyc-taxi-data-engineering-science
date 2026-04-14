with dim_rate_codes as (
    select distinct rate_code_id from {{ ref('stg_nyc_taxi') }}
)

select
    rate_code_id as rate_code_key,
    case rate_code_id
        when 1 then 'Standard rate'
        when 2 then 'JFK'
        when 3 then 'Newark'
        when 4 then 'Nassau or Westchester'
        when 5 then 'Negotiated fare'
        when 6 then 'Group ride'
        else 'Unknown'
    end as rate_code_description
from dim_rate_codes