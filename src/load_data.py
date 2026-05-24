import sqlite3
import pandas as pd
import os
from pathlib import Path
from config import COUNTRIES, START_YEAR, END_YEAR, DB_PATH, RAW_CSV_PATH


def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)

    schema_path = Path(__file__).parent.parent / "sql" / "schema.sql"
    with open(schema_path, 'r') as f:
        schema = f.read()
        conn.executescript(schema)

    conn.close()
    print("Database created")


def load_energy_data():
    conn = sqlite3.connect(DB_PATH)

    csv_file = RAW_CSV_PATH
    df = pd.read_csv(csv_file)

    df = df[df['iso_code'].isin(COUNTRIES)]
    df = df[(df['year'] >= START_YEAR) & (df['year'] <= END_YEAR)]

    print(f"Loading {len(df)} rows")

    # energy_consumption: skip rows where primary_energy_consumption is NaN
    df_consumption = (
        df.loc[df['primary_energy_consumption'].notna(),
               ['iso_code', 'year', 'primary_energy_consumption']]
        .rename(columns={
            'iso_code': 'country_code',
            'primary_energy_consumption': 'total_consumption_twh',
        })
    )

    # renewable_energy: one row per country/year
    df_renewable = (
        df[['iso_code', 'year', 'renewables_share_energy',
            'solar_electricity', 'wind_electricity', 'hydro_electricity']]
        .rename(columns={
            'iso_code': 'country_code',
            'renewables_share_energy': 'renewable_percentage',
            'solar_electricity': 'solar_electricity_twh',
            'wind_electricity': 'wind_electricity_twh',
            'hydro_electricity': 'hydro_electricity_twh',
        })
    )

    # energy_production: melt wide-long, drop NaN/zero rows, compute percentage
    source_cols = {
        'Coal': 'coal_electricity',
        'Natural Gas': 'gas_electricity',
        'Oil': 'oil_electricity',
        'Nuclear': 'nuclear_electricity',
        'Solar': 'solar_electricity',
        'Wind': 'wind_electricity',
        'Hydro': 'hydro_electricity',
        'Biomass': 'biofuel_electricity',
    }
    df_long = df[
        ['iso_code', 'year', 'electricity_generation'] + list(source_cols.values())
    ].melt(
        id_vars=['iso_code', 'year', 'electricity_generation'],
        value_vars=list(source_cols.values()),
        var_name='source_col',
        value_name='production_twh',
    )
    df_long['energy_source'] = df_long['source_col'].map({v: k for k, v in source_cols.items()})
    df_long = df_long[df_long['production_twh'].notna() & (df_long['production_twh'] > 0)].copy()
    total = df_long['electricity_generation']
    df_long['percentage_of_total'] = (
        (df_long['production_twh'] / total.where(total > 0) * 100).fillna(0)
    )
    df_production = (
        df_long[['iso_code', 'year', 'energy_source', 'production_twh', 'percentage_of_total']]
        .rename(columns={'iso_code': 'country_code'})
    )

    with conn:
        df_consumption.to_sql('energy_consumption', conn, if_exists='append', index=False)
        df_renewable.to_sql('renewable_energy', conn, if_exists='append', index=False)
        df_production.to_sql('energy_production', conn, if_exists='append', index=False)

    expected_counts = {"countries": 8, "energy_consumption": 40, "renewable_energy": 40}
    for table, expected in expected_counts.items():
        actual = pd.read_sql(f"SELECT COUNT(*) as n FROM {table}", conn).iloc[0, 0]
        assert actual == expected, f"{table}: expected {expected} rows, got {actual}"

    conn.close()
    print("Data loaded")


def show_summary():
    conn = sqlite3.connect(DB_PATH)

    print("\n=== Summary ===")

    query = "SELECT COUNT(*) as count FROM countries"
    print(f"countries: {pd.read_sql(query, conn)['count'][0]} rows")

    query = "SELECT COUNT(*) as count FROM energy_production"
    print(f"energy_production: {pd.read_sql(query, conn)['count'][0]} rows")

    query = "SELECT COUNT(*) as count FROM energy_consumption"
    print(f"energy_consumption: {pd.read_sql(query, conn)['count'][0]} rows")

    query = "SELECT COUNT(*) as count FROM renewable_energy"
    print(f"renewable_energy: {pd.read_sql(query, conn)['count'][0]} rows")

    print("\n=== Renewable Energy 2023 ===")
    query = """
        SELECT c.country_name, re.renewable_percentage,
               re.solar_electricity_twh, re.wind_electricity_twh
        FROM renewable_energy re 
        JOIN countries c ON re.country_code = c.country_code 
        WHERE re.year = 2023 AND re.renewable_percentage IS NOT NULL
        ORDER BY re.renewable_percentage DESC
    """
    print(pd.read_sql(query, conn).to_string())

    conn.close()


if __name__ == "__main__":
    print("Loading Energy Data\n")
    create_database()
    load_energy_data()
    show_summary()
    print("\nDone!")