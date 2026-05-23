# European Energy Market Analysis Dashboard

> SQL-based analysis of energy production, consumption, and renewable adoption across 8 European countries (2020-2024)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-SQLite-orange.svg)](https://www.sqlite.org/)
[![Data](https://img.shields.io/badge/Data-OWID-green.svg)](https://github.com/owid/energy-data)

> A SQL-driven analysis of European energy markets (8 countries, 2020–2024) with a tested ETL load and an interactive Streamlit dashboard.

## Project Overview

This project analyzes European energy markets to identify trends in renewable adoption, fossil fuel reduction, and progress toward 2030 climate targets. Built as a portfolio demonstration of SQL, data analysis, and business insight generation skills.

**Key Finding**: No European country is currently on track to meet 2030 renewable energy targets at current growth rates. Belgium would need to accelerate renewable growth by 7x to meet commitments.

## Dashboard overview:
![img.png](dashboard/img.png)
![img_1.png](dashboard/img_1.png)
![img_2.png](dashboard/img_2.png)
![img_3.png](dashboard/img_3.png)
![img_4.png](dashboard/img_4.png)
![img_5.png](dashboard/img_5.png)
![img_6.png](dashboard/img_6.png)

## Structure:
![img.png](dashboard/structure.png)

## Key Insights

### 1. Netherlands Led the Fastest Fossil Fuel Exit

Netherlands cut its fossil fuel share from 69.8% (2020) to 49.2% (2023) — a 20.6 percentage-point
reduction, the largest among the 8 countries. Belgium came second in relative terms (−23%), while
Germany's fossil share was essentially unchanged (44.3% → 44.2%) despite its large absolute renewable
capacity.

### 2. Germany Dominates Renewable Output; Netherlands Leads Per Capita

Germany generated 222.6 TWh of renewable electricity in 2023 — roughly 3× more than any neighbor
in absolute terms. Per-capita the ranking flips: Netherlands leads at 2.82 TWh/million people,
Germany second (2.42), Belgium third (2.01). France sits last at 1.04 due to heavy nuclear dependence.

### 3. No Country Is On Track for 2030

Belgium's renewable share is declining (−0.7% annually) while it needs +5.2%/year to reach its
42.5% target — projecting to just 7.3% by 2030. Germany (current 24%, target 50%) projects to
26.2%. All 8 countries in the dataset are classified BEHIND at current growth rates.

[Full analysis with business implications →](docs/KEY_INSIGHTS.md)

## Database Structure

```
Countries (8)
├── BEL (Belgium)
├── FRA (France)  
├── NLD (Netherlands)
├── DEU (Germany)
└── ... 4 more

Energy Production (299 records)
├── By source: Solar, Wind, Hydro, Nuclear, Coal, Gas, Oil
└── 2020-2024 data

Renewable Energy (40 records)
├── Renewable percentage
└── Solar/Wind/Hydro electricity generation

Energy Consumption (40 records)
└── Total consumption by country/year
```

## SQL Queries

### 1. Fossil Fuel Reduction Analysis
Identifies which countries reduced fossil fuel dependency most since 2020.

**Key Technique**: CTEs, aggregation, percentage calculations

```sql
WITH fossil_2020 AS (...)
SELECT country_name, 
       fossil_pct_2020, 
       fossil_pct_2023,
       (fossil_pct_2020 - fossil_pct_2023) as reduction
FROM fossil_2020 JOIN fossil_2023
ORDER BY reduction DESC;
```

**Result**: Netherlands (-29.5%), Belgium (-23.2%), Poland (-11.3%)

### 2. Renewable Energy Trends
Analyzes renewable energy adoption and electricity generation over time.

**Key Technique**: JOINs, time series analysis

**Result**: Germany dominates absolute production (222 TWh), Netherlands leads per capita (2.8 TWh/M)

### 3. Belgium vs Neighbors Comparison  
Compares Belgium to France, Netherlands, Germany on renewable metrics.

**Key Technique**: Window functions (RANK), per-capita calculations

**Result**: Belgium ranks 3rd of 4 in renewable capacity per capita

### 4. Energy Demand Patterns
Tracks consumption trends and year-over-year growth.

**Key Technique**: Window functions (LAG), growth rate calculations

**Result**: 2022-2024 shows declining consumption across most countries (-1% to -8%)

### 5. 2030 Climate Targets Tracking
Projects whether countries will meet renewable energy targets.

**Key Technique**: Multiple CTEs, growth projections, conditional logic

**Result**: All 8 countries currently behind targets, requiring 2-5x acceleration

## Technical Stack

- **Database**: SQLite
- **Language**: Python 3.9+
- **Libraries**: pandas, sqlite3
- **Data Source**: Our World in Data (OWID)
- **Analysis**: 5 complex SQL queries with CTEs, window functions, aggregations

## Getting Started

**Data source:** [Our World in Data — Energy Dataset](https://github.com/owid/energy-data), aggregated from the Energy Institute Statistical Review, Ember, and Eurostat. The raw CSV is not stored in this repo and must be downloaded before loading the database.

### Prerequisites
- Python 3.9+

### Installation

```bash
git clone https://github.com/lizakolosova/european-energy-market-analysis-dashboard.git
cd european-energy-market-analysis-dashboard
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Download raw data (~7 MB CSV)
python scripts/download_data.py

# Build the database
python load_data.py

# Verify the load
pytest tests/

# Launch the dashboard
streamlit run dashboard.py
```

### Run Analysis

```bash
python run_queries.py
```

## Skills Demonstrated

- SQL analysis: CTEs, window functions (RANK, LAG), conditional aggregation across 5 business questions
- Data quality testing with pytest: 10 assertions covering row counts, FK integrity, and value ranges
- Configuration management: single source of truth for all constants, paths, and targets
- Interactive dashboards with Streamlit and Plotly
- Reproducible setup: automated data download, deterministic DB load, tests that verify the result
- Working with real-world public datasets (Our World in Data)

## Use Cases

This analysis is relevant for:
- **Energy Policy Analysts**: Track renewable adoption progress
- **Investment Firms**: Identify renewable growth opportunities
- **Consulting**: Benchmark country performance
- **Government**: Assess policy effectiveness

## Data Source

Data sourced from [Our World in Data - Energy Dataset](https://github.com/owid/energy-data), which aggregates:
- Energy Institute Statistical Review
- Ember Yearly Electricity Data
- Eurostat

**Coverage**: 8 EU countries, 2020-2024, 40 data points, 299 production records

