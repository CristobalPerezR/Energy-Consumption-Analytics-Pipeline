import pandas as pd
import os
from pandera.dtypes import DateTime
from pandera.pandas import DataFrameSchema, Column
from ..utils.db import get_connection, insert_dataframe
from ..utils.errors import InsertionError, ValidationError

processed_schema = DataFrameSchema({
    "datetime": Column(DateTime, nullable=False),
    "global_active_power": Column(float, nullable=True, coerce=True),
    "global_reactive_power": Column(float, nullable=True, coerce=True),
    "voltage": Column(float, nullable=True, coerce=True),
    "global_intensity": Column(float, nullable=True, coerce=True),
    "sub_metering_1": Column(float, nullable=True, coerce=True),
    "sub_metering_2": Column(float, nullable=True, coerce=True),
    "sub_metering_3": Column(float, nullable=True, coerce=True),
    "is_missing_power": Column(int, nullable=False, coerce=True),
    "hour" : Column(int, nullable=False, coerce=True),
    "day_of_week": Column(int, nullable=False, coerce=True),
    "is_weekend": Column(int, nullable=False, coerce=True),
    "has_missing": Column(int, nullable=False, coerce=True),
})

def load_processed(df:pd.DataFrame) -> int:
    csv_dir = os.path.join("data", "processed")
    os.makedirs(csv_dir, exist_ok=True)
    csv_path = os.path.join(csv_dir, "household_power_consumption_processed.csv")

    with get_connection() as conn:
        try: 
            valid_df = processed_schema.validate(df)
            print("Load_Process: Schema validated")
            try:
                insert_dataframe(conn, valid_df, "household_power_processed")
                print("Load_Process: Dataframe inserted into table: [household_power_processed]")

                valid_df.to_csv(csv_path, sep=";", index=False)
                print(f"Load_Process: csv saved at: {csv_path}")

            except Exception as e:
                raise InsertionError(f"Load_Process: Insertion failed: {e}")
        except Exception as e:
            raise ValidationError(f"Load_Process: Schema not valid: {e}")
        
    return 1