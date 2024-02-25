{{
    config(
        materialized='table'
    )
}}

select

    {{ dbt_utils.generate_surrogate_key(['dispatching_base_num', 'pickup_datetime']) }} as tripid,
    {{ dbt.safe_cast("pu_location_id", api.Column.translate_type("integer")) }} as pickup_locationid,
    {{ dbt.safe_cast("DOlocationID", api.Column.translate_type("integer")) }} as dropoff_locationid,
    
    -- timestamps
    timestamp_micros(CAST(pickup_datetime / 1000 AS INT64)) as pickup_datetime,
    timestamp_micros(CAST(dropoff_datetime / 1000 AS INT64)) as dropoff_datetime,
    pickup_date,
    
    -- trip info
    {{ dbt.safe_cast("sr_flag", api.Column.translate_type("integer")) }} as sr_flag,
    dispatching_base_num as dispatching_base,
    affiliated_base_number as affilated_base

from {{ source('staging','ny_fhv_2019') }}
where pickup_date >= '2019-01-01' and pickup_date < '2020-01-01'

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}