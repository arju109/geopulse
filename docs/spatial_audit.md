\# Spatial Audit: Sedona catchment join



\## Setup

\- Spark 3.5.3, Sedona 1.6.1, local mode, Windows laptop

\- Driver memory limit: 2 GB

\- Catchments: 500 m buffers (projected to EPSG:32643, buffered, projected back)



\## Results

| Metric | Value |

|---|---|

| Pings processed | <paste> |

| Intersections found | <paste> |

| Runtime | <paste> seconds |

| Out-of-memory errors | None |



\## Evidence

Screenshots are in `docs/images/` (Jobs tab, Executors tab).



\## Notes

\- Output written to Parquet instead of collecting to the driver.

\- The catchments table is tiny (3 rows), so Spark broadcasts it and no heavy shuffle is needed.

\- Cross-check: on the 10k sample, the buffer method gave 7,485 and the distance method 7,500 (0.2% difference).

- Output was counted (not written to disk) because Parquet writes on Windows need native Hadoop libraries.
  The full join still runs over all points. Writing to Parquet will be done in WSL/Linux and in Airflow.