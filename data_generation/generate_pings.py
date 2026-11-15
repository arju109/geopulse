"""Generate realistic mock mobile pings for Gandhinagar.
Usage: python data_generation/generate_pings.py [n_pings] [n_devices]
"""
import sys
import numpy as np
import pandas as pd

n = int(sys.argv[1]) if len(sys.argv) > 1 else 3_000_000
n_dev = int(sys.argv[2]) if len(sys.argv) > 2 else 20_000
rng = np.random.default_rng(42)

stores = pd.DataFrame({
    "store_id": ["S1", "S2", "S3"],
    "store_name": ["Store A", "Store B", "Store C"],
    "latitude": [23.2200, 23.2260, 23.2000],
    "longitude": [72.6500, 72.6560, 72.6300],
})
S = stores[["latitude", "longitude"]].to_numpy()
LAT0, LAT1, LON0, LON1 = 23.17, 23.27, 72.60, 72.70

# Each device has a home and a workplace
home = np.column_stack([rng.uniform(LAT0, LAT1, n_dev), rng.uniform(LON0, LON1, n_dev)])
group = rng.choice(4, n_dev, p=[0.30, 0.20, 0.15, 0.35])   # works near S1, S2, S3, or elsewhere
work = np.column_stack([rng.uniform(LAT0, LAT1, n_dev), rng.uniform(LON0, LON1, n_dev)])
for g in range(3):
    m = group == g
    work[m] = S[g] + rng.normal(0, 0.0025, (m.sum(), 2))     # ~250 m spread

# Half of the Store A workers pass Store B on their morning commute
has_via = (group == 0) & (rng.random(n_dev) < 0.5)

dev = rng.integers(0, n_dev, n)
period = rng.choice(4, n, p=[0.35, 0.35, 0.15, 0.15])        # morning, evening, midday, night
t = rng.random(n)
day = rng.integers(0, 7, n)

h, w = home[dev], work[dev]
mid = (h + w) / 2
via = np.where(has_via[dev][:, None], S[1], mid)

def path(a, v, b, t):
    first = (t < 0.5)[:, None]
    return np.where(first, a + (2 * t)[:, None] * (v - a), v + (2 * t - 1)[:, None] * (b - v))

morning = path(h, via, w, t)       # home -> (Store B or midpoint) -> work
evening = path(w, mid, h, t)       # work -> home
midday = w + rng.normal(0, 0.0008, (n, 2))
night = h + rng.normal(0, 0.0008, (n, 2))

conds = [period == 0, period == 1, period == 2, period == 3]
pos = np.select([c[:, None] for c in conds], [morning, evening, midday, night])
pos = pos + rng.normal(0, 0.0003, (n, 2))                    # GPS noise ~30 m

night_minutes = np.r_[np.arange(1200, 1440), np.arange(0, 360)]
minutes = np.select(
    conds,
    [450 + t * 120,                       # morning 07:30-09:30
     990 + t * 120,                       # evening 16:30-18:30
     rng.uniform(660, 900, n),            # midday 11:00-15:00
     rng.choice(night_minutes, n)],       # night
).astype(int)

ts = (pd.Timestamp("2026-01-12")
      + pd.to_timedelta(day, unit="D")
      + pd.to_timedelta(minutes, unit="m"))

pings = pd.DataFrame({
    "device_id": np.char.add("dev_", np.char.zfill(dev.astype(str), 6)),
    "latitude": pos[:, 0].round(6),
    "longitude": pos[:, 1].round(6),
    "ping_ts": ts,
})

pings.to_parquet(f"spark_sedona/sample_data/pings_real_{n}.parquet", index=False)
stores.to_csv("spark_sedona/sample_data/stores_sample.csv", index=False)

print(f"{len(pings):,} pings, {n_dev:,} devices written")
print("Pings per hour (should spike at 7-9 and 16-18):")
print(pings.ping_ts.dt.hour.value_counts().sort_index().to_string())