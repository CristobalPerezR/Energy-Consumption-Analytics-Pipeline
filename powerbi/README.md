# Power BI Dashboard – Household Energy Consumption

## Data Source
The dashboard is built using the output of the ETL pipeline:
- `data/processed/household_power_consumption_processed.csv`

## Pages Overview

### 1. Overview
**KPIs**
- Average Voltage: 240.84 V
- Average Global Active Power: 1.09 kW

**Visuals**
- Consumption distribution by sub-metering
- Average consumption per hour

**Key Insight**
Peak consumption occurs between 18:00 and 22:00, reaching values close to 2.0 kW.

---

### 2. Drill-down Analysis
**Filters**
- Hour selector (0–23)
- Day of week

**Visuals**
- Sub-metering contribution per day
- Average consumption per day of the week
- Hourly consumption matrix

**Key Insights**
- Heating/AC dominates consumption (~70–80%) across all days.
- Slightly higher average consumption during weekends.
- Clear morning (7–8) and evening (19–21) consumption peaks.

---

### 3. Data Quality
**Visuals**
- Missing data distribution by day of week
- Missing data per hour
- Complete vs incomplete records

**Key Insights**
- Overall data completeness is high (≈98.8%).
- Missing values show temporal patterns, peaking around morning and midday hours.

## Intended Use
This dashboard is designed for:
- Exploratory analysis
- Consumption pattern identification
- Data quality monitoring

It is not intended for real-time monitoring or operational forecasting.