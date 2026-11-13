import pandas as pd

def test_output_has_contract_columns():
    df = pd.read_csv("spark_sedona/sample_data/ping_store_intersections.csv")
    assert list(df.columns) == ["device_id", "store_id", "ping_ts", "latitude", "longitude"]
    assert len(df) > 0
    assert df.store_id.isin(["S1", "S2", "S3"]).all()