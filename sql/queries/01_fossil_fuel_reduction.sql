-- Business Question 1: Which EU countries reduced fossil fuel dependency most since 2020?
-- This query calculates the change in fossil fuel percentage from 2020 to 2023

WITH fossil_2020 AS (
    SELECT 
        ep.country_code,
        c.country_name,
        SUM(CASE WHEN es.category = 'Fossil' THEN ep.percentage_of_total ELSE 0 END) as fossil_pct_2020
    FROM energy_production ep
    JOIN countries c ON ep.country_code = c.country_code
    JOIN energy_sources es ON ep.energy_source = es.source_name
    WHERE ep.year = 2020
    GROUP BY ep.country_code, c.country_name
),
fossil_2023 AS (
    SELECT 
        ep.country_code,
        SUM(CASE WHEN es.category = 'Fossil' THEN ep.percentage_of_total ELSE 0 END) as fossil_pct_2023
    FROM energy_production ep
    JOIN energy_sources es ON ep.energy_source = es.source_name
    WHERE ep.year = 2023
    GROUP BY ep.country_code
)
SELECT 
    f20.country_name,
    ROUND(f20.fossil_pct_2020, 2) as fossil_pct_2020,
    ROUND(f23.fossil_pct_2023, 2) as fossil_pct_2023,
    ROUND(f20.fossil_pct_2020 - f23.fossil_pct_2023, 2) as reduction_points,
    ROUND(((f20.fossil_pct_2020 - f23.fossil_pct_2023) / f20.fossil_pct_2020 * 100), 2) as pct_reduction
FROM fossil_2020 f20
JOIN fossil_2023 f23 ON f20.country_code = f23.country_code
WHERE f20.fossil_pct_2020 > 0
ORDER BY reduction_points DESC;
