-- Renewable metrics per country per year: renewable percentage alongside solar, wind, hydro
-- breakdown and total primary energy consumption. Joins renewable_energy and energy_consumption.

SELECT
    c.country_name,
    re.year,
    ROUND(re.renewable_percentage, 2) as renewable_pct,
    ROUND(ec.total_consumption_twh, 2) as consumption_twh,
    ROUND(re.solar_electricity_twh, 2) as solar_twh,
    ROUND(re.wind_electricity_twh, 2) as wind_twh,
    ROUND(re.hydro_electricity_twh, 2) as hydro_twh,
    ROUND((re.solar_electricity_twh + re.wind_electricity_twh + re.hydro_electricity_twh), 2) as total_renewable_twh
FROM renewable_energy re
JOIN countries c ON re.country_code = c.country_code
JOIN energy_consumption ec ON re.country_code = ec.country_code
    AND re.year = ec.year
WHERE re.renewable_percentage IS NOT NULL
ORDER BY c.country_name, re.year;
