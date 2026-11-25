\# Mid-Project Demo Script (about 3 minutes)



\## 1. Problem (20 s)

Retailers open stores based on static data and risk cannibalizing existing locations. GeoPulse uses mobile pings to measure it.



\## 2. Spatial audit (60 s)

\- Show `docs/spatial\_audit.md` and the Spark UI screenshots.

\- Run: `python spark\_sedona\\jobs\\catchment\_audit.py 2g`

\- Point out: 3,000,000 pings, 594,855 intersections, about 7 s, 2 GB driver memory, no out-of-memory error. Identical counts at 2g and 4g.



\## 3. dbt integrity check (60 s)

\- Show `dbt run` and `dbt test` passing.

\- In Snowsight, run the hourly profile query: peaks at 7-9 and 16-18.



\## 4. Business insight (30 s)

\- Show `FCT\_CANNIBALIZATION`: "X% of Store A's devices also visit Store B" (use your real number).



\## 5. Next steps (10 s)

Kepler.gl dashboard with H3 hexagons and a 24-hour slider, then the Airflow DAG.

