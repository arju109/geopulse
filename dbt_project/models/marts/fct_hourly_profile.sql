-- Total unique visitors per hour of day across all stores, labelled by period
with hourly as (
    select
        hour_of_day,
        sum(unique_visitors) as visitors,
        sum(pings)           as pings
    from {{ ref('fct_hourly_visitors') }}
    group by 1
)
select
    hour_of_day,
    visitors,
    pings,
    case
        when hour_of_day between 7 and 9   then 'morning_peak'
        when hour_of_day between 16 and 18 then 'evening_peak'
        else 'off_peak'
    end as period
from hourly