import time
from sedona.spark import SedonaContext

UTM = "EPSG:32643"
RADIUS_M = 500
PINGS = "spark_sedona/sample_data/pings_big_2000000.parquet"
OUT = "spark_sedona/sample_data/audit_output"

config = (
    SedonaContext.builder()
    .appName("geopulse-audit")
    .config("spark.jars.packages",
            "org.apache.sedona:sedona-spark-shaded-3.5_2.12:1.6.1,"
            "org.datasyslab:geotools-wrapper:1.6.1-28.2")
    .config("spark.driver.memory", "2g")            # the memory limit we are proving
    .config("spark.sql.shuffle.partitions", "8")
    .getOrCreate()
)
sedona = SedonaContext.create(config)

stores = sedona.read.csv("spark_sedona/sample_data/stores_sample.csv", header=True, inferSchema=True)
pings = sedona.read.parquet(PINGS)
stores.createOrReplaceTempView("stores")
pings.createOrReplaceTempView("pings")
n_pings = pings.count()

start = time.time()

sedona.sql(f"""
  SELECT store_id,
         ST_Transform(
           ST_Buffer(ST_Transform(ST_Point(longitude, latitude), 'EPSG:4326', '{UTM}'), {RADIUS_M}),
           '{UTM}', 'EPSG:4326') AS catchment
  FROM stores
""").createOrReplaceTempView("catchments")

result = sedona.sql("""
  SELECT p.device_id, c.store_id, p.ping_ts, p.latitude, p.longitude
  FROM pings p
  JOIN catchments c
    ON ST_Contains(c.catchment, ST_Point(p.longitude, p.latitude))
""")

# Write to disk instead of toPandas(), so nothing is pulled into memory
n_hits = result.count()          # forces the full 2M-point join, nothing written to disk

elapsed = time.time() - start
print("=" * 50)
print(f"Pings processed:       {n_pings:,}")
print(f"Driver memory limit:   2g")
print(f"Intersections found:   {n_hits:,}")
print(f"Runtime (join+write):  {elapsed:.1f} seconds")
print("=" * 50)

input("Job finished. Open http://localhost:4040 for screenshots, then press Enter to exit...")