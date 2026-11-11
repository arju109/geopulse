\# GeoPulse Data Contract



\## Rules

\- Coordinates: Sedona uses (longitude, latitude) order. Columns are always named `latitude` and `longitude`.

\- CRS: all stored coordinates are EPSG:4326 (WGS84).

\- Timestamps: UTC, format `YYYY-MM-DD HH:MM:SS`.

\- Mock city: <agree on one city with Member 1>, with 2-3 stores.



\## Table: RAW\_PINGS (Member 1)

| Column | Type |

|---|---|

| device\_id | STRING (anonymized) |

| latitude | FLOAT |

| longitude | FLOAT |

| ping\_ts | TIMESTAMP |

| geog | GEOGRAPHY |



\## Table: STORES (Member 1)

| Column | Type |

|---|---|

| store\_id | STRING |

| store\_name | STRING |

| latitude | FLOAT |

| longitude | FLOAT |



\## Table: PING\_STORE\_INTERSECTIONS (Member 2, output)

| Column | Type |

|---|---|

| device\_id | STRING |

| store\_id | STRING |

| ping\_ts | TIMESTAMP |

| latitude | FLOAT |

| longitude | FLOAT |



\## Sample data (needed by day 2)

Member 1 provides `spark\_sedona/sample\_data/pings\_sample.csv` (about 10k rows) and `stores\_sample.csv` (3 stores).

