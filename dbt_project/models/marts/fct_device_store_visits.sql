-- One row per device and store: how many pings fall inside the 500 m catchment
select
    p.device_id,
    s.store_id,
    count(*)                                                   as pings,
    count_if(hour(p.ping_ts) between 7 and 9)                  as morning_pings,
    count(distinct date_trunc('day', p.ping_ts))               as days_visited
from {{ source('raw', 'raw_pings') }} p
join {{ source('raw', 'stores') }} s
  on st_dwithin(p.geog, s.geog, 500)
group by 1, 2