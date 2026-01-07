from src.etl.extract import extract_validate_save
from src.etl.transform import rawdb_transformation
from src.etl.load import load_processed
from src.dataset.download import download_unzip
from src.db_script.init_db import init_db

print("\n================= DOWNLOAD PROCESS =================\n")

file_path = download_unzip()

print("\n================= DB INITIALIZATION =================\n")

init_db("household_power")

print("\n================= EXTRACTION PROCESS =================\n")

extract_validate_save(file_path)

print("\n================= TRANSFORMATION PROCESS =================\n")

df = rawdb_transformation()

print("\n================= LOAD PROCESS =================\n")

load_processed(df)

print("\n================= ETL FINISHED =================\n")