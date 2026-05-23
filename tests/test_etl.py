from pathlib import Path

SQL_DIR = Path(__file__).parent.parent / "sql" / "queries"


def test_countries_table_has_exactly_8_rows(db):
    (count,) = db.execute("SELECT COUNT(*) FROM countries").fetchone()
    assert count == 8, f"Expected 8 countries, got {count}"


def test_energy_consumption_has_40_rows(db):
    (count,) = db.execute("SELECT COUNT(*) FROM energy_consumption").fetchone()
    assert count == 40, (
        f"Expected 40 rows (8 countries × 5 years = 40), got {count}"
    )


def test_renewable_energy_has_40_rows(db):
    (count,) = db.execute("SELECT COUNT(*) FROM renewable_energy").fetchone()
    assert count == 40, (
        f"Expected 40 rows (8 countries × 5 years = 40), got {count}"
    )


def test_energy_production_has_299_rows(db):
    (count,) = db.execute("SELECT COUNT(*) FROM energy_production").fetchone()
    assert count == 299, (
        f"Expected 299 production rows (up to 8 sources × 8 countries × 5 years, "
        f"minus zero-value sources that are skipped at load time), got {count}"
    )


def test_no_null_country_codes_in_any_table(db):
    for table in ("energy_production", "energy_consumption", "renewable_energy"):
        (count,) = db.execute(
            f"SELECT COUNT(*) FROM {table} WHERE country_code IS NULL"
        ).fetchone()
        assert count == 0, f"Found {count} NULL country_code(s) in {table}"


def test_renewable_percentage_between_0_and_100(db):
    (bad_count,) = db.execute("""
        SELECT COUNT(*) FROM renewable_energy
        WHERE renewable_percentage IS NOT NULL
          AND (renewable_percentage < 0 OR renewable_percentage > 100)
    """).fetchone()
    assert bad_count == 0, f"Found {bad_count} rows with renewable_percentage outside [0, 100]"


def test_all_production_country_codes_exist_in_countries_table(db):
    (count,) = db.execute("""
        SELECT COUNT(*)
        FROM energy_production ep
        LEFT JOIN countries c ON ep.country_code = c.country_code
        WHERE c.country_code IS NULL
    """).fetchone()
    assert count == 0, (
        f"Found {count} row(s) in energy_production whose country_code "
        f"has no matching entry in the countries table"
    )


def test_all_years_within_expected_range(db):
    for table in ("energy_production", "energy_consumption", "renewable_energy"):
        min_year, max_year = db.execute(
            f"SELECT MIN(year), MAX(year) FROM {table}"
        ).fetchone()
        assert min_year >= 2020, (
            f"{table}: earliest year {min_year} is before the expected start of 2020"
        )
        assert max_year <= 2024, (
            f"{table}: latest year {max_year} is after the expected end of 2024"
        )

    for table in ("energy_consumption", "renewable_energy"):
        present = {
            row[0]
            for row in db.execute(f"SELECT DISTINCT year FROM {table}").fetchall()
        }
        expected = {2020, 2021, 2022, 2023, 2024}
        assert present == expected, (
            f"{table}: expected years {sorted(expected)}, "
            f"got {sorted(present)}"
        )


def test_query_05_returns_all_8_countries(db):
    sql_path = SQL_DIR / "05_2030_targets_tracking.sql"
    assert sql_path.exists(), f"SQL file not found: {sql_path}"
    sql = sql_path.read_text(encoding="utf-8")
    rows = db.execute(sql).fetchall()
    assert len(rows) == 8, (
        f"Query 05 should return one row per country (8 total), got {len(rows)}"
    )


def test_no_duplicate_country_year_pairs_in_consumption(db):
    rows = db.execute("""
        SELECT country_code, year, COUNT(*) as cnt
        FROM energy_consumption
        GROUP BY country_code, year
        HAVING COUNT(*) > 1
    """).fetchall()
    assert len(rows) == 0, (
        f"Found duplicate (country_code, year) pairs in energy_consumption: {rows}"
    )
