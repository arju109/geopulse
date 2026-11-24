\# GeoPulse Architecture



\## Pipeline

```

Python generator -> Parquet pings

&#x20;       |

&#x20;       +--> Sedona/PySpark: 500 m catchments, spatial join, scale audit

&#x20;       |

&#x20;       +--> Snowflake RAW (RAW\_PINGS, STORES with GEOGRAPHY)

&#x20;                  |

&#x20;            dbt models (MART schema)

&#x20;              - fct\_hourly\_visitors   unique visitors per store per hour

&#x20;              - fct\_hourly\_profile    morning vs evening vs off-peak

&#x20;              - fct\_device\_store\_visits, fct\_cannibalization

&#x20;                  |

&#x20;            Kepler.gl React dashboard (H3 hexagons, 24 h slider)   \[planned]

&#x20;       Airflow DAG: Spark -> load -> dbt, daily                    \[planned]

```



\## Components

| Layer | Tool | Output |

|---|---|---|

| Data synthesis | Python (numpy, pandas) | Parquet of 3M pings, 20,000 devices, 3 stores |

| Spatial processing | Apache Sedona 1.6.1 on PySpark 3.5.3 | Ping-store intersections |

| Warehouse | Snowflake (GEOGRAPHY) | RAW and MART schemas |

| Modeling | dbt-snowflake | Hourly visitors, cannibalization |

| Dashboard | Kepler.gl + React | Planned |

| Orchestration | Airflow | Planned |



\## Catchment logic

Latitude and longitude are in degrees, so a 500 m buffer needs a metric CRS. Sedona projects points to EPSG:32643 (UTM 43N), buffers 500 m, and projects back to EPSG:4326. Sedona uses (longitude, latitude) order. Snowflake uses `ST\_DWITHIN(geog\_a, geog\_b, 500)`, which measures in metres on GEOGRAPHY.



\## Validation

\- Buffer method vs great-circle distance on 10k pings: 7,485 vs 7,500 (0.2% difference).

\- Scale audit: 3,000,000 pings, 594,855 intersections at both 2g and 4g driver memory, about 7 s, no out-of-memory errors.

\- dbt tests: not-null, accepted values, and a singular test that peak hours exceed off-peak by 1.5x.

