from src.etl.extract import Extract_validate
from src.db_script.init_db import init_db

init_db("household_power")
df = Extract_validate("data/raw/household_power_consumption.txt")