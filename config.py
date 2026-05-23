from pathlib import Path

COUNTRIES = ["BEL", "FRA", "NLD", "DEU", "POL", "ESP", "ITA", "SWE"]
START_YEAR = 2020
END_YEAR = 2024
TARGET_YEAR = 2030
DB_PATH = Path(__file__).parent / "data" / "energy.db"
RAW_CSV_PATH = Path(__file__).parent / "data" / "raw" / "owid-energy-data.csv"

# Per-country 2030 renewable energy targets (% of primary energy from renewables).
# Source: EU Fit for 55 package + national energy and climate plans (NECPs).
# Values cross-checked against sql/queries/05_2030_targets_tracking.sql.
TARGETS_2030 = {
    "BEL": 42.5,
    "FRA": 40.0,
    "NLD": 45.0,
    "DEU": 50.0,
    "POL": 32.0,
    "ESP": 48.0,
    "ITA": 40.0,
    "SWE": 65.0,
}
