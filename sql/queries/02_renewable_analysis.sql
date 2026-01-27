-- Business Question 2: What's the correlation between renewable energy adoption and electricity prices?
-- This query provides data for correlation analysis between renewable % and prices

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

-- Follow-up analysis in Python:
-- 1. Calculate Pearson correlation coefficient
-- 2. Create scatter plot: renewable_percentage vs household_price
-- 3. Linear regression to predict price based on renewable %
-- 4. Segment analysis: high renewables (>40%) vs low renewables (<20%)

-- Expected insights:
-- - Do countries with more renewables have higher/lower prices?
-- - Has this relationship changed over time (2020 vs 2023)?
-- - Are there outliers? (e.g., France with nuclear = low prices despite less renewables)
