-- Table 1: Country Information
CREATE TABLE IF NOT EXISTS countries (
    country_code VARCHAR(2) PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL,
    region VARCHAR(50),
    population_millions DECIMAL(10,2),
    gdp_billions_eur DECIMAL(12,2)
);

INSERT INTO countries (country_code, country_name, region, population_millions) VALUES
    ('BEL', 'Belgium', 'Western Europe', 11.6),
    ('FRA', 'France', 'Western Europe', 67.8),
    ('NLD', 'Netherlands', 'Western Europe', 17.5),
    ('DEU', 'Germany', 'Western Europe', 83.2),
    ('POL', 'Poland', 'Eastern Europe', 38.0),
    ('ESP', 'Spain', 'Southern Europe', 47.4),
    ('ITA', 'Italy', 'Southern Europe', 59.0),
    ('SWE', 'Sweden', 'Northern Europe', 10.5);

-- Table 2: Energy Production (by source)
CREATE TABLE IF NOT EXISTS energy_production (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code VARCHAR(3) NOT NULL,
    year INTEGER NOT NULL,
    energy_source VARCHAR(50) NOT NULL,
    production_twh DECIMAL(10,2),
    percentage_of_total DECIMAL(5,2),
    FOREIGN KEY (country_code) REFERENCES countries(country_code),
    UNIQUE(country_code, year, energy_source)
);

-- Table 3: Energy Consumption
CREATE TABLE IF NOT EXISTS energy_consumption (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code VARCHAR(3) NOT NULL,
    year INTEGER NOT NULL,
    total_consumption_twh DECIMAL(10,2),
    FOREIGN KEY (country_code) REFERENCES countries(country_code),
    UNIQUE(country_code, year)
);

-- Table 4: Renewable Energy Metrics
CREATE TABLE IF NOT EXISTS renewable_energy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code VARCHAR(3) NOT NULL,
    year INTEGER NOT NULL,
    renewable_percentage DECIMAL(5,2),
    solar_electricity_twh DECIMAL(8,2),
    wind_electricity_twh DECIMAL(8,2),
    hydro_electricity_twh DECIMAL(8,2),
    FOREIGN KEY (country_code) REFERENCES countries(country_code),
    UNIQUE(country_code, year)
);

-- Table 5: Energy Sources Reference
CREATE TABLE IF NOT EXISTS energy_sources (
    source_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name VARCHAR(50) UNIQUE NOT NULL,
    category VARCHAR(20),
    is_renewable BOOLEAN
);

INSERT INTO energy_sources (source_name, category, is_renewable) VALUES
    ('Solar', 'Renewable', 1),
    ('Wind', 'Renewable', 1),
    ('Hydro', 'Renewable', 1),
    ('Biomass', 'Renewable', 1),
    ('Geothermal', 'Renewable', 1),
    ('Natural Gas', 'Fossil', 0),
    ('Coal', 'Fossil', 0),
    ('Oil', 'Fossil', 0),
    ('Nuclear', 'Nuclear', 0),
    ('Other', 'Other', 0);