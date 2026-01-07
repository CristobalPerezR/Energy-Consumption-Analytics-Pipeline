# Energy Consumption Analytics Pipeline

This repository contains an ETL pipeline to process and analyze household electricity consumption data, based on the UCI dataset: [Individual household electric power consumption](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption).

The objective is to prepare clean and consistent data, ready for exploratory analysis and visualization in Power BI.

## Repository Structure
```
data/
│
├── raw/           # Raw data downloaded
├── processed/     # Processed data through ETL pipeline
└── database/      # SQLite DB
notebooks/         # Exploration
sql/
│ ├── schema.sql   # Tables definitions
src/
│ ├── dataset/     # Download function
│ ├── db_script/   # Database initialization
│ ├── etl/         # Extract, Transform, Load
│ └── utils/       # Auxiliary functions (DB, errors)
```
## Requirements
- Python 3.10+
- Main libraries:
  - `pandas`
  - `pandera`
  - `sqlite3`
  - `requests`

Dependencies Installation
```bash
pip install -r requirements.txt
```

## Pipeline ETL
This pipeline consists of three main steps

1. Extract
    * Read original dataset.
    * Schema validation through `pandera`.
    * Insert into the `household_power_raw` table in the DB.
2. Transform
    * Merge of `Date` and `Time` into `datetime`.
    * Calculate basic features and flags.
        * `is_missing_power`: indicate if there is a NaN in `Global_active_power`.
        * `hour`, `day_of_week`, `is_weekend`.
        * `has_missing`: indicate if there is a NaN in any row.
3. Load
    * Schema validation for processed DataFrame.
    * Insert into table `household_power_processed` from DB.
    * Export to CSV at `data/processed/household_power_consumption_processed.csv`.

### Pipeline execution
```bash
python -m run_etl_pipeline.py
```

### Pipeline Flow

Download & Unzip → DB Initialization → Extract → Transform → Load → CSV Output

## Database Schema
* **household_power_raw** → raw data table
* **household_power_processed** → processed data table

Columns for household_power_processed:

| Column                | Description                                      |
| --------------------- | ------------------------------------------------ |
| datetime              | Combined date and time                           |
| global_active_power   | Global active power (kilowatts)                  |
| global_reactive_power | Global reactive power (kilowatts)                |
| voltage               | Voltage (volts)                                  |
| global_intensity      | Global current intensity (amperes)               |
| sub_metering_1, 2, 3  | Energy sub-metering (watt-hour of active energy) |
| is_missing_power      | Flag indicating if `global_active_power` is NaN  |
| hour                  | Hour of the day (0–23)                           |
| day_of_week           | Day of the week (0=Monday … 6=Sunday)            |
| is_weekend            | Flag if the day is weekend (0=No / 1=Yes)        |
| has_missing           | Flag if any column in the row is NaN             |