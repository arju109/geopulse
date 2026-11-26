import sys
import time
from sedona.spark import SedonaContext

MEM = sys.argv[1] if len(sys.argv) > 1 else "2g"
UTM = "EPSG:32643"
RADIUS_M = 500
PINGS = "spark_sedona/sample_data/pings_real_3000000.parquet"
STORES = "spark_sedona/sample_data/stores_sample.csv"

config = (
    SedonaContext.builder()
    .appName("geopulse-audit")
    .config("spark.jars.packages",
            "org.apache.sedona:sedona-spark-shaded-3.5_2.12:1.6.1,"
            "org.datasyslab:geotools-wrapper:1.6.1-28.2")
    .config("spark.driver.memory", MEM)
    .config("spark.sql.shuffle.partitions", "8")
    .getOrCreate()
)
sedona = SedonaContext.create(config)

stores = sedona.read.csv(STORES, header=True, inferSchema=True)
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

n_hits = result.count()   # forces the full join; nothing is written to disk
elapsed = time.time() - start

print("=" * 50)
print(f"Pings processed:       {n_pings:,}")
print(f"Driver memory limit:   {MEM}")
print(f"Intersections found:   {n_hits:,}")
print(f"Runtime (join+count):  {elapsed:.1f} seconds")
print("=" * 50)