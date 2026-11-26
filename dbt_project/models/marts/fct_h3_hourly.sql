-- Unique devices and pings per H3 hexagon (resolution 9, ~170 m edge) per hour
with cells as (
    select
        device_id,
        date_trunc('hour', ping_ts)                      as hour_ts,
        hour(ping_ts)                                    as hour_of_day,
        h3_point_to_cell_string(geog, 9)                 as h3_cell
    from {{ source('raw', 'raw_pings') }}
)
select
    h3_cell,
    h3_cell_to_boundary(h3_cell)                         as boundary,
    hour_of_day,
    count(distinct device_id)                            as unique_devices,
    count(*)                                             as pings
from cells
group by h3_cell, hour_of_day