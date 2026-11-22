with visits as (
    select * from {{ ref('fct_device_store_visits') }}
),
store_totals as (
    select store_id, count(distinct device_id) as devices
    from visits
    group by 1
),
pairs as (
    select
        a.store_id as store_a,
        b.store_id as store_b,
        count(distinct a.device_id) as shared_devices,
        count(distinct case when a.morning_pings > 0 then a.device_id end) as shared_morning_devices
    from visits a
    join visits b
      on a.device_id = b.device_id
     and a.store_id <> b.store_id
    group by 1, 2
)
select
    p.store_a,
    p.store_b,
    t.devices                                            as store_a_devices,
    p.shared_devices,
    round(100.0 * p.shared_devices / t.devices, 1)       as pct_of_a_also_visiting_b,
    p.shared_morning_devices,
    round(100.0 * p.shared_morning_devices / t.devices, 1) as pct_morning_overlap
from pairs p
join store_totals t on t.store_id = p.store_a