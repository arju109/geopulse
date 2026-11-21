-- Unique visitors per store per hour, using a 500 m catchment (ST_DWITHIN on GEOGRAPHY, metres)
select
    s.store_id,
    s.store_name,
    date_trunc('hour', p.ping_ts) as hour_ts,
    hour(p.ping_ts)               as hour_of_day,
    count(distinct p.device_id)   as unique_visitors,
    count(*)                      as pings
from {{ source('raw', 'raw_pings') }} p
join {{ source('raw', 'stores') }} s
  on st_dwithin(p.geog, s.geog, 500)
group by 1, 2, 3, 4