from sedona.spark import SedonaContext

UTM = "EPSG:32643"   # metric CRS for Gujarat (72E-78E)
RADIUS_M = 500

config = (
    SedonaContext.builder()
    .appName("geopulse-catchments")
    .config("spark.jars.packages",
            "org.apache.sedona:sedona-spark-shaded-3.5_2.12:1.6.1,"
            "org.datasyslab:geotools-wrapper:1.6.1-28.2")
    .getOrCreate()
)
sedona = SedonaContext.create(config)

stores = sedona.read.csv("spark_sedona/sample_data/stores_sample.csv", header=True, inferSchema=True)
pings = sedona.read.csv("spark_sedona/sample_data/pings_sample.csv", header=True, inferSchema=True)
stores.createOrReplaceTempView("stores")
pings.createOrReplaceTempView("pings")

# 500 m catchments: project to metres, buffer, project back
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

# Cross-check using a different method (great-circle distance)
check = sedona.sql(f"""
  SELECT COUNT(*) AS n FROM pings p JOIN stores s
  ON ST_DistanceSphere(ST_Point(p.longitude, p.latitude), ST_Point(s.longitude, s.latitude)) <= {RADIUS_M}
""").collect()[0]["n"]

n = result.count()
print(f"Intersections (buffer method):   {n}")
print(f"Intersections (distance method): {check}")
print("Per store:")
result.groupBy("store_id").count().show()

result.toPandas().to_csv("spark_sedona/sample_data/ping_store_intersections.csv", index=False)