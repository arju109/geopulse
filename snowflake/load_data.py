"""Load stores and pings into Snowflake. Usage: python snowflake/load_data.py [n_rows]"""
import os, sys
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

load_dotenv()
N = int(sys.argv[1]) if len(sys.argv) > 1 else 500_000   # start small

conn = snowflake.connector.connect(
    account=os.environ["SNOWFLAKE_ACCOUNT"], user=os.environ["SNOWFLAKE_USER"],
    password=os.environ["SNOWFLAKE_PASSWORD"], warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
    database=os.environ["SNOWFLAKE_DATABASE"], schema=os.environ["SNOWFLAKE_SCHEMA"],
)
cur = conn.cursor()

# Stores
stores = pd.read_csv("spark_sedona/sample_data/stores_sample.csv")
stores.columns = [c.upper() for c in stores.columns]
cur.execute("TRUNCATE TABLE STORES")
write_pandas(conn, stores, "STORES")
cur.execute("UPDATE STORES SET geog = TO_GEOGRAPHY('POINT(' || longitude || ' ' || latitude || ')')")

# Pings
pings = pd.read_parquet("spark_sedona/sample_data/pings_real_3000000.parquet").head(N)
pings["ping_ts"] = pings["ping_ts"].dt.strftime("%Y-%m-%d %H:%M:%S")
pings.columns = [c.upper() for c in pings.columns]
cur.execute("TRUNCATE TABLE RAW_PINGS")
write_pandas(conn, pings, "RAW_PINGS", chunk_size=200_000)
cur.execute("UPDATE RAW_PINGS SET geog = TO_GEOGRAPHY('POINT(' || longitude || ' ' || latitude || ')') WHERE geog IS NULL")

cur.execute("SELECT COUNT(*) FROM RAW_PINGS")
print("RAW_PINGS rows:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM STORES")
print("STORES rows:", cur.fetchone()[0])
conn.close()