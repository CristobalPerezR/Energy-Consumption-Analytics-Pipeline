CREATE TABLE IF NOT EXISTS household_power_raw  (
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    global_active_power REAL,
    global_reactive_power REAL,
    voltage REAL,
    global_intensity REAL,
    sub_metering_1 REAL,
    sub_metering_2 REAL,
    sub_metering_3 REAL
);

CREATE TABLE IF NOT EXISTS household_power_processed (
    DateTime DATETIME PRIMARY KEY,
    Global_active_power REAL,
    Global_reactive_power REAL,
    Voltage REAL,
    Global_intensity REAL,
    Sub_metering_1 REAL,
    Sub_metering_2 REAL,
    Sub_metering_3 REAL,
    is_missing_power INTEGER,
    hour INTEGER,
    day_of_week INTEGER,
    is_weekend INTEGER
)