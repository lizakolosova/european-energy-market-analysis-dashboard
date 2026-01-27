import sqlite3
import pandas as pd
import os
from pathlib import Path

DB_PATH = "data/energy.db"
RAW_DATA_PATH = "data/raw"


def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)

    with open('sql/schema.sql', 'r') as f:
        schema = f.read()
        conn.executescript(schema)

    conn.close()
    print("Database created")


def load_energy_data():
    conn = sqlite3.connect(DB_PATH)

    csv_file = Path(RAW_DATA_PATH) / "owid-energy-data.csv"
    df = pd.read_csv(csv_file)

    countries = ['BEL', 'FRA', 'NLD', 'DEU', 'POL', 'ESP', 'ITA', 'SWE']
    df = df[df['iso_code'].isin(countries)]
    df = df[df['year'] >= 2020]

    print(f"Loading {len(df)} rows")

    for _, row in df.iterrows():
        country = row['iso_code']
        year = int(row['year'])

        if pd.notna(row.get('primary_energy_consumption')):
            conn.execute("""
                INSERT INTO energy_consumption (country_code, year, total_consumption_twh)
                VALUES (?, ?, ?)
            """, (country, year, row['primary_energy_consumption']))

        conn.execute("""
            INSERT INTO renewable_energy 
            (country_code, year, renewable_percentage, solar_electricity_twh, wind_electricity_twh, hydro_electricity_twh)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            country,
            year,
            row.get('renewables_share_energy'),
            row.get('solar_electricity'),
            row.get('wind_electricity'),
            row.get('hydro_electricity')
        ))

        total_elec = row.get('electricity_generation', 0)

        sources = {
            'Coal': row.get('coal_electricity'),
            'Natural Gas': row.get('gas_electricity'),
            'Oil': row.get('oil_electricity'),
            'Nuclear': row.get('nuclear_electricity'),
            'Solar': row.get('solar_electricity'),
            'Wind': row.get('wind_electricity'),
            'Hydro': row.get('hydro_electricity'),
            'Biomass': row.get('biofuel_electricity')
        }

        for source, value in sources.items():
            if pd.notna(value) and value > 0:
                percentage = (value / total_elec * 100) if total_elec > 0 else 0
                conn.execute("""
                    INSERT INTO energy_production 
                    (country_code, year, energy_source, production_twh, percentage_of_total)
                    VALUES (?, ?, ?, ?, ?)
                """, (country, year, source, value, percentage))

    conn.commit()
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