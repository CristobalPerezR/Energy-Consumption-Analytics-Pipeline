import pandas as pd
import sqlite3
from pandera.pandas import DataFrameSchema, Column

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

def Extract_validate_save(data):
    df = pd.read_csv(data, sep=";", na_values="?")

    try:
        valid = raw_schema.validate(df)
        print("Schema validated")
        return 1
    except Exception as e:
        print("Schema not valid")
        print(e)
        return 0