-- Business Question 4: Peak demand patterns by season and country
-- Note: This requires monthly/seasonal data. If only annual data available, 
-- this query shows annual consumption patterns and highlights peak analysis approach

SELECT 
    c.country_name,
    ec.year,
    ROUND(ec.total_consumption_twh, 2) as consumption_twh,
    ROUND(ec.total_consumption_twh / c.population_millions, 2) as consumption_per_capita_twh,
    LAG(ec.total_consumption_twh) OVER (PARTITION BY c.country_code ORDER BY ec.year) as prev_year_consumption,
    ROUND(((ec.total_consumption_twh - LAG(ec.total_consumption_twh) OVER (PARTITION BY c.country_code ORDER BY ec.year)) /
           LAG(ec.total_consumption_twh) OVER (PARTITION BY c.country_code ORDER BY ec.year) * 100), 2) as yoy_growth_pct
FROM energy_consumption ec
JOIN countries c ON ec.country_code = c.country_code
WHERE c.country_code IN ('BEL', 'FRA', 'NLD', 'DEU', 'POL')
ORDER BY c.country_name, ec.year;

-- Peak demand insights (for dashboard highlights):
-- 1. Which countries have highest per-capita consumption?
-- 2. Is consumption growing or declining?
-- 3. What % is residential vs industrial? (indicates economic structure)
-- 4. Belgium-specific: How does consumption compare to production capacity?

-- For monthly data analysis (if available from ENTSOE or Elia):
-- CREATE TABLE monthly_demand (
--     country_code VARCHAR(2),
--     year INTEGER,
--     month INTEGER,
--     consumption_gwh DECIMAL(10,2)
-- );
-- 
-- Then calculate seasonal peaks:
-- SELECT 
--     country_code,
--     year,
--     CASE 
--         WHEN month IN (12,1,2) THEN 'Winter'
--         WHEN month IN (3,4,5) THEN 'Spring'
--         WHEN month IN (6,7,8) THEN 'Summer'
--         ELSE 'Autumn'
--     END as season,
--     SUM(consumption_gwh) as seasonal_consumption
-- FROM monthly_demand
-- GROUP BY country_code, year, season;
