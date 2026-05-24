import sqlite3
import pandas as pd
from pathlib import Path
from config import DB_PATH

conn = sqlite3.connect(DB_PATH)

queries = [
    ('01_fossil_fuel_reduction.sql', 'Fossil Fuel Reduction (2020-2023)'),
    ('02_renewable_metrics.sql', 'Renewable Energy Metrics'),
    ('03_belgium_neighbor_comparison.sql', 'Belgium vs Neighbors'),
    ('04_demand_patterns.sql', 'Energy Demand Patterns'),
    ('05_2030_targets_tracking.sql', '2030 Renewable Targets Progress')
]

_ROOT = Path(__file__).parent.parent

for filename, title in queries:
    filepath = _ROOT / 'sql' / 'queries' / filename

    if not filepath.exists():
        print(f"Skipping {filename} - file not found")
        continue

    print("\n" + "=" * 70)
    print(f"QUERY: {title}")
    print("=" * 70)

    with open(filepath, 'r') as f:
        sql = f.read()

    try:
        result = pd.read_sql(sql, conn)
        print(result.to_string(index=False))

        output_file = _ROOT / 'sql' / 'results' / f"results_{filename.replace('.sql', '.txt')}"
        with open(output_file, 'w', encoding='utf-8') as out:
            out.write(f"{title}\n")
            out.write("=" * 70 + "\n\n")
            out.write(result.to_string(index=False))

        print(f"\nSaved to: {output_file.relative_to(_ROOT)}")

    except Exception as e:
        print(f"Error: {e}")

conn.close()

print("\n" + "=" * 70)
print("ALL QUERIES COMPLETE!")
print("=" * 70)