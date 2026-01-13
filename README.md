# Energy Consumption Analytics Pipeline

This repository contains an ETL pipeline to process and analyze household electricity consumption data, based on the UCI dataset: [Individual household electric power consumption](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption).

The objective is to prepare clean and consistent data to support analytics, exploratory analysis, and baseline machine learning modeling, while enabling downstream visualization and reporting in Power BI.

`(ETL → BI | ETL → ML)`

## Repository Structure
```
README.md
requirements.txt
run_etl_pipeline.py
run_ml_pipeline.py

data/
├── raw/                # Original dataset (txt / zip)
├── processed/          # Output of ETL pipeline
│   └── household_power_consumption_processed.csv
├── database/           # SQLite database
│   └── household_power.db
└── ml/                 # Machine learning artifacts
    ├── ml_ready.csv    # Feature-engineered dataset
    ├── metrics.json    # Evaluation metrics
    └── models/
        ├── linear_model.joblib
        ├── ridge_model.joblib
        └── scaler.joblib

notebooks/
└── exploration.ipynb   # Exploratory analysis

sql/
└── schema.sql          # Database schema

src/
├── dataset/
│   └── download.py     # Dataset download
├── db_script/
│   └── init_db.py      # Database initialization
├── etl/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── features/
│   └── build_features.py   # ML feature engineering
├── ml/
│   └── train_baseline.py   # Linear & Ridge training
└── utils/
    ├── db.py
    └── errors.py
```
## Requirements
- Python 3.10+
- Main libraries:
  - `pandas`
  - `pandera`
  - `numpy`
  - `requests`
  - `scikit-learn`
  - `joblib`

Dependencies Installation
```bash
pip install -r requirements.txt
```

## Considerations
The following files will be created during pipeline execution due to their size:
* ETL pipeline:
    * `data/raw/household_power_consumption.zip`
    * `data/raw/household_power_consumption.txt`
    * `data/processed/household_power_consumption_processed.csv`
* ML pipeline:
    * `data/ml/ml_ready.csv`


## Pipeline ETL
This pipeline consists of three main steps:

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

## Machine Learning Pipeline

After the ETL process, a baseline machine learning pipeline is executed to predict household energy consumption.

### Objective

Predict `global_active_power` using temporal and rolling statistical features derived from historical consumption.

### Feature Engineering

The ML dataset is generated from the processed ETL output and includes:
* Cyclical time encoding:
    + `hour_sin`, `hour_cos`.
    + `day_of_week_sin`, `day_of_week_cos`.
* Calendar features:
    + `is_weekend`.
* Rolling statistics:
    + `global_active_power_ma_5m`.
    + `global_active_power_ma_15m`.
    + `global_active_power_ma_30m`.

The resulting dataset is stored at: `data/ml/ml_ready.csv`

### Models
Two baseline regression models are trained:
* Linear Regression
* Ridge Regression

Before training:
* Data is split chronologically (70% train / 30% test)
* Features are standardized using StandardScaler

### Evaluation Metrics

Models are evaluated using:
* RMSE (Root Mean Squared Error)
* MAE (Mean Absolute Error)

Metrics are save to `data/ml/metrics.json`.

Trained models and scaler are persisted using `joblib` and stored at:`data/ml/models/`

### ML pipeline execution
```bash
python -m run_ml_pipeline.py
```

### Pipeline Flow

Load processed CSV → Feature engineering → Save ml_ready.csv → Train models → Save metrics & models (JSON & joblib)


## Power BI Analytics

A Power BI dashboard was built on top of the processed dataset to analyze household energy consumption patterns and data quality.

### Dashboard Pages
- **Overview**: High-level KPIs and hourly consumption patterns.
- **Drill-down Analysis**: Detailed consumption breakdown by hour, day of week, and sub-metering.
- **Data Quality**: Missing data distribution across days and hours.

The dashboard focuses on:
- Identifying peak consumption hours.
- Understanding sub-metering contribution (Kitchen, Laundry, Heating/AC).
- Evaluating data completeness and temporal missing patterns.

Detailed dashboard documentation and insights are available at: [README BI](https://github.com/CristobalPerezR/Energy-Consumption-Analytics-Pipeline/blob/main/powerbi/README.md)
