"""Generate N mock pings as Parquet (compact). Usage: python make_big_data.py 2000000"""
import sys
import numpy as np
import pandas as pd

n = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
rng = np.random.default_rng(7)

# City-wide scatter around three stores plus background noise
centers = np.array([[23.2200, 72.6500], [23.2260, 72.6560], [23.2000, 72.6300]])
idx = rng.integers(0, 3, n)
noise = rng.random(n) < 0.3                      # 30% scattered across the city
lat = centers[idx, 0] + rng.normal(0, 0.004, n)
lon = centers[idx, 1] + rng.normal(0, 0.004, n)
lat[noise] = rng.uniform(23.15, 23.28, noise.sum())
lon[noise] = rng.uniform(72.58, 72.72, noise.sum())

hours = rng.choice([8, 9, 10, 12, 14, 17, 18, 19], n, p=[.2, .2, .1, .05, .05, .15, .15, .1])
ts = pd.Timestamp("2026-01-12") + pd.to_timedelta(hours * 60 + rng.integers(0, 60, n), unit="m")

df = pd.DataFrame({
    "device_id": ["dev_" + str(i) for i in rng.integers(0, 200_000, n)],
    "latitude": lat.round(6), "longitude": lon.round(6), "ping_ts": ts,
})
"""Generate N mock pings as Parquet (compact). Usage: python make_big_data.py 2000000"""
import sys
import numpy as np
import pandas as pd

n = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
rng = np.random.default_rng(7)

# City-wide scatter around three stores plus background noise
centers = np.array([[23.2200, 72.6500], [23.2260, 72.6560], [23.2000, 72.6300]])
idx = rng.integers(0, 3, n)
noise = rng.random(n) < 0.3                      # 30% scattered across the city
lat = centers[idx, 0] + rng.normal(0, 0.004, n)
lon = centers[idx, 1] + rng.normal(0, 0.004, n)
lat[noise] = rng.uniform(23.15, 23.28, noise.sum())
lon[noise] = rng.uniform(72.58, 72.72, noise.sum())

hours = rng.choice([8, 9, 10, 12, 14, 17, 18, 19], n, p=[.2, .2, .1, .05, .05, .15, .15, .1])
ts = pd.Timestamp("2026-01-12") + pd.to_timedelta(hours * 60 + rng.integers(0, 60, n), unit="m")

df = pd.DataFrame({
    "device_id": ["dev_" + str(i) for i in rng.integers(0, 200_000, n)],
    "latitude": lat.round(6), "longitude": lon.round(6), "ping_ts": ts,
})
"""Generate N mock pings as Parquet (compact). Usage: python make_big_data.py 2000000"""
import sys
import numpy as np
import pandas as pd

n = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
rng = np.random.default_rng(7)

# City-wide scatter around three stores plus background noise
centers = np.array([[23.2200, 72.6500], [23.2260, 72.6560], [23.2000, 72.6300]])
idx = rng.integers(0, 3, n)
noise = rng.random(n) < 0.3                      # 30% scattered across the city
lat = centers[idx, 0] + rng.normal(0, 0.004, n)
lon = centers[idx, 1] + rng.normal(0, 0.004, n)
lat[noise] = rng.uniform(23.15, 23.28, noise.sum())
lon[noise] = rng.uniform(72.58, 72.72, noise.sum())

hours = rng.choice([8, 9, 10, 12, 14, 17, 18, 19], n, p=[.2, .2, .1, .05, .05, .15, .15, .1])
ts = pd.Timestamp("2026-01-12") + pd.to_timedelta(hours * 60 + rng.integers(0, 60, n), unit="m")

df = pd.DataFrame({
    "device_id": ["dev_" + str(i) for i in rng.integers(0, 200_000, n)],
    "latitude": lat.round(6), "longitude": lon.round(6), "ping_ts": ts,
})
df.to_parquet(f"spark_sedona/sample_data/pings_big_{n}.parquet", index=False,
              coerce_timestamps="us", allow_truncated_timestamps=True)