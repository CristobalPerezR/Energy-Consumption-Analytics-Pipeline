import pandas as pd
from pandera.dtypes import DateTime
from ..utils.db import get_connection

orden_column = [
    "datetime",
    "global_active_power",
    "global_reactive_power",
    "voltage",
    "global_intensity",
    "sub_metering_1",
    "sub_metering_2",
    "sub_metering_3",
    "is_missing_power",
    "hour",
    "day_of_week",
    "is_weekend",
    "has_missing"
]

def rawdb_transformation() -> pd.DataFrame:

    with get_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM household_power_raw", conn)

    print("Transform_Process: data extracted from household_power_raw")

    df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], format="%d/%m/%Y %H:%M:%S")
    df.drop(columns=["date", "time"], inplace=True)

    df["is_missing_power"] = df["global_active_power"].isna().astype(int)
    df["hour"] = df["datetime"].dt.hour
    df["day_of_week"] = df["datetime"].dt.dayofweek
    df["is_weekend"] = df["day_of_week"].isin([5,6]).astype(int)

    df["has_missing"] = df.isna().any(axis=1)

    print("Transform_Process: Transforms done")

    df = df[orden_column]

    return df