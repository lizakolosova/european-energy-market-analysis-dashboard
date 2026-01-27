-- Business Question 3: How does Belgium compare to neighbors in solar/wind capacity?
-- Focus countries: Belgium, France, Netherlands, Germany (Western Europe neighbors)

WITH neighbor_comparison AS (
    SELECT 
        c.country_name,
        re.year,
        re.solar_electricity_twh,
        re.wind_electricity_twh,
        (re.solar_electricity_twh + re.wind_electricity_twh) as total_renewable_twh,
        re.renewable_percentage,
        ROUND(re.solar_electricity_twh / c.population_millions, 3) as solar_per_capita,
        ROUND(re.wind_electricity_twh / c.population_millions, 3) as wind_per_capita,
        ROUND((re.solar_electricity_twh + re.wind_electricity_twh) / c.population_millions, 3) as renewable_per_capita
    FROM renewable_energy re
    JOIN countries c ON re.country_code = c.country_code
    WHERE c.country_code IN ('BEL', 'FRA', 'NLD', 'DEU')
)
SELECT
    country_name,
    year,
    ROUND(solar_electricity_twh, 2) as solar_twh,
    ROUND(wind_electricity_twh, 2) as wind_twh,
    ROUND(total_renewable_twh, 2) as total_renewable_twh,
    ROUND(renewable_percentage, 2) as renewable_pct,
    solar_per_capita,
    wind_per_capita,
    renewable_per_capita,
    RANK() OVER (PARTITION BY year ORDER BY renewable_per_capita DESC) as capacity_rank
FROM neighbor_comparison
ORDER BY year DESC, renewable_per_capita DESC;

-- Key insights to highlight:
-- - Belgium's absolute capacity vs neighbors
-- - Per-capita comparison (important for fair comparison given different country sizes)
-- - Growth trends: Is Belgium catching up or falling behind?
-- - Which technology (solar vs wind) is Belgium focusing on?
