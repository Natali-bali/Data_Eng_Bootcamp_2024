{{
    config(
        materialized='table'
    )
}}

with fhv_data as (
    select *,
        'FHV' as service_type 
    from {{ ref('stg_fhv_tripdata') }}
),

fhv as (
    select * from fhv_data 
    where pickup_locationid is not null
    and
    dropoff_locationid is not null
),
 
dim_zones as ( 
    select * from {{ ref('dim_zones') }}
)

select fhv.tripid, 
    fhv.service_type,
    fhv.pickup_locationid, 
    pickup_zones.borough as pickup_borough, 
    pickup_zones.zone as pickup_zone, 
    fhv.dropoff_locationid,
    dropoff_zones.borough as dropoff_borough, 
    dropoff_zones.zone as dropoff_zone,  
    fhv.pickup_datetime, 
    fhv.dropoff_datetime, 
    fhv.pickup_date, 
    fhv.sr_flag, 
    fhv.dispatching_base, 
    fhv.affilated_base   
from fhv
inner join dim_zones as pickup_zones
on fhv.pickup_locationid = pickup_zones.locationid
inner join dim_zones as dropoff_zones
on fhv.dropoff_locationid = dropoff_zones.locationid