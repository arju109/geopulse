# Spatial Audit: Sedona Catchment Join

## Setup
- Spark 3.5.3 and Apache Sedona 1.6.1, local mode, Windows laptop
- Driver memory limit: 2 GB
- Shuffle partitions: 8
- Catchments: 500 m buffers around each store (points projected to EPSG:32643, buffered by 500 m, projected back to EPSG:4326)
- Join: `ST_Contains(catchment, ST_Point(longitude, latitude))`

## Results (2 million pings)
| Metric | Value |
|---|---|
| Pings processed | 2,000,000 |
| Stores / catchments | 3 |
| Intersections found | 790,367 |
| Driver memory limit | 2 GB |
| Runtime (full join + count) | 3.9 seconds |
| Out-of-memory errors | None |

## Validation
On the 10,000-ping sample, the buffer method found 7,485 intersections and a separate great-circle distance method found 7,500. The 0.2% difference is expected (projected circle vs spherical distance), which confirms the coordinate order and projection are correct.

## Notes
- The full join ran over all 2M points using `result.count()`. Output was counted instead of written to disk, because Parquet writes on Windows need native Hadoop libraries (`hadoop.dll` not loadable by Java). Parquet output will be tested in WSL/Linux and in Airflow.
- The catchments table has only 3 rows, so Spark broadcasts it and no heavy shuffle is needed.
- Overlapping catchments (S1 and S2) mean one ping can match more than one store, so intersections can exceed what a single-store count suggests.

## Evidence
Spark UI screenshots (Jobs and Executors tabs) will be added in `docs/images/` on Day 2.

## Next
- Scale test with 5M pings at 2g and 4g driver memory (Day 3).