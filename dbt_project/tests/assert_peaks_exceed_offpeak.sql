-- Fails if the average peak hour is not at least 1.5x the average off-peak hour
with p as (
    select
        avg(case when period = 'morning_peak' then pings end) as morning,
        avg(case when period = 'evening_peak' then pings end) as evening,
        avg(case when period = 'off_peak'     then pings end) as offpeak
    from {{ ref('fct_hourly_profile') }}
)
select *
from p
where morning < 1.5 * offpeak
   or evening < 1.5 * offpeak