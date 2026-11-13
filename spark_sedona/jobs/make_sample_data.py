"""Creates a small mock dataset so Member 2 can work before Member 1 delivers."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

stores = pd.DataFrame({
    "store_id": ["S1", "S2", "S3"],
    "store_name": ["Store A", "Store B", "Store C"],
    "latitude": [23.2200, 23.2260, 23.2000],
    "longitude": [72.6500, 72.6560, 72.6300],
})  # S1 and S2 are ~900 m apart, so their 500 m catchments overlap

N_DEVICES, N_PINGS = 500, 10_000
devices = [f"dev_{i:04d}" for i in range(N_DEVICES)]
rows = []
for _ in range(N_PINGS):
    dev = rng.choice(devices)
    k = int(dev[-4:])
    # each device has a "home store"; 25% of devices also visit S1/S2 both
    store_idx = k % 3
    if k % 4 == 0:
        store_idx = rng.choice([0, 1])
    s = stores.iloc[store_idx]
    # ~300 m spread around the store (0.003 deg is roughly 300 m)
    lat = s.latitude + rng.normal(0, 0.003)
    lon = s.longitude + rng.normal(0, 0.003)
    # morning and evening commuter peaks
    hour = int(rng.choice([8, 9, 10, 17, 18, 19, 12, 14], p=[.2, .2, .1, .15, .15, .1, .05, .05]))
    ts = pd.Timestamp("2026-01-12") + pd.Timedelta(hours=hour, minutes=int(rng.integers(0, 60)))
    rows.append((dev, round(lat, 6), round(lon, 6), ts))

pings = pd.DataFrame(rows, columns=["device_id", "latitude", "longitude", "ping_ts"])
stores.to_csv("spark_sedona/sample_data/stores_sample.csv", index=False)
pings.to_csv("spark_sedona/sample_data/pings_sample.csv", index=False)
print(len(pings), "pings,", len(stores), "stores written")