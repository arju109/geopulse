\# dbt Data Integrity Check



\- dbt compiles and runs successfully against Snowflake (GEOPULSE.MART).

\- Model `fct\_hourly\_visitors`: unique visitors per store per hour (500 m catchment, ST\_DWITHIN).

\- Model `fct\_hourly\_profile`: visitors per hour of day, labelled morning peak (7-9), evening peak (16-18), off-peak.

\- Singular test `assert\_peaks\_exceed\_offpeak`: average peak-hour pings must be at least 1.5x off-peak.



\## Result

All tests passed (see screenshot).



!\[dbt test](images/dbt\_test\_pass.png)







Hourly profile: paste the Snowsight table here (or a summary: peaks at hours 7-9 and 16-18).

