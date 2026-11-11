\# GeoPulse: Hyper-Local Retail Mobility Analytics



Pipeline: mock GPS pings -> Snowflake -> Sedona/PySpark catchment joins -> dbt models -> Kepler.gl dashboard, orchestrated by Airflow.



\## Team

| Member | Area | Folder |

|---|---|---|

| 1 | Data synthesis + Snowflake | data\_generation/, snowflake/ |

| 2 | Sedona/PySpark + Airflow | spark\_sedona/, airflow/ |

| 3 | dbt + cannibalization | dbt\_project/ |

| 4 | Kepler.gl / React | dashboard/ |



\## Rules

1\. Never commit directly to `main`. Use branches like `member2/feature-name`.

2\. Merge through Pull Requests with one reviewer.

3\. Never commit credentials. Copy `.env.example` to `.env` and fill it locally.

4\. Commit small and often.

