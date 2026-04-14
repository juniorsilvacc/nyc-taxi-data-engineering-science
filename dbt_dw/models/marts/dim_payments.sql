with dim_payments as (
    select distinct payment_type_id from {{ ref('stg_nyc_taxi') }}
)

select 
    payment_type_id as payment_key,
    case payment_type_id
        when 1 then 'Credit card'
        when 2 then 'Cash'
        when 3 then 'No charge'
        when 4 then 'Dispute'
        when 5 then 'Unknown'
        when 6 then 'Voided trip'
        else 'Empty'
    end as payment_description
from dim_payments