import pandas as pd
from pandera.pandas import DataFrameSchema, Column
from ..utils.db import get_connection, insert_dataframe
from ..utils.errors import InsertionError, ValidationError

raw_schema = DataFrameSchema({
    "Date": Column(str, nullable=False),
    "Time": Column(str, nullable=False),

    "Global_active_power": Column(float, nullable=True, coerce=True),
    "Global_reactive_power": Column(float, nullable=True, coerce=True),
    "Voltage": Column(float, nullable=True, coerce=True),
    "Global_intensity": Column(float, nullable=True, coerce=True),
    "Sub_metering_1": Column(float, nullable=True, coerce=True),
    "Sub_metering_2": Column(float, nullable=True, coerce=True),
    "Sub_metering_3": Column(float, nullable=True, coerce=True),
})

def extract_validate_save(data_path: str) -> int:
    df = pd.read_csv(data_path, sep=";", na_values="?")
    try:
        valid = raw_schema.validate(df)
        print("Extract_Process: Schema validated")
        try:
            with get_connection() as conn:
                insert_dataframe(conn, valid, "household_power_raw")
            print("Extract_Process: Dataframe inserted into table: [household_power_raw]")
        except Exception as e:
            raise InsertionError(f"Extract_Process: Insertion failed: {e}")
        return 1
    except Exception as e:
        raise ValidationError(f"Extract_Process: Schema not valid: {e}")