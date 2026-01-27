-- Business Question 5: Which countries are on track to meet 2030 renewable energy targets?
-- EU 2030 target: 42.5% renewable energy (Fit for 55 package)
-- Individual country targets vary

WITH country_targets AS (
    SELECT 'BEL' as country_code, 42.5 as target_2030_pct UNION ALL
    SELECT 'FRA', 40.0 UNION ALL
    SELECT 'NLD', 45.0 UNION ALL
    SELECT 'DEU', 50.0 UNION ALL
    SELECT 'POL', 32.0 UNION ALL
    SELECT 'ESP', 48.0 UNION ALL
    SELECT 'ITA', 40.0 UNION ALL
    SELECT 'SWE', 65.0
),
current_progress AS (
    SELECT
        country_code,
        year,
        renewable_percentage,
        LAG(renewable_percentage) OVER (PARTITION BY country_code ORDER BY year) as prev_year_pct,
        renewable_percentage - LAG(renewable_percentage) OVER (PARTITION BY country_code ORDER BY year) as annual_growth
    FROM renewable_energy
    WHERE year >= 2020
),
latest_progress AS (
    SELECT
        cp.country_code,
        c.country_name,
        cp.year,
        cp.renewable_percentage as current_pct,
        ct.target_2030_pct,
        (ct.target_2030_pct - cp.renewable_percentage) as gap_to_target,
        AVG(cp.annual_growth) OVER (PARTITION BY cp.country_code) as avg_annual_growth,
        (2030 - cp.year) as years_remaining,
        (ct.target_2030_pct - cp.renewable_percentage) / (2030 - cp.year) as required_annual_growth
    FROM current_progress cp
    JOIN countries c ON cp.country_code = c.country_code
    JOIN country_targets ct ON cp.country_code = ct.country_code
    WHERE cp.year = (SELECT MAX(year) FROM current_progress WHERE country_code = cp.country_code)
)
SELECT
    country_name,
    ROUND(current_pct, 2) as current_renewable_pct,
    target_2030_pct,
    ROUND(gap_to_target, 2) as gap_to_target,
    ROUND(avg_annual_growth, 2) as avg_growth_rate,
    ROUND(required_annual_growth, 2) as required_growth_rate,
    CASE
        WHEN avg_annual_growth >= required_annual_growth THEN 'ON TRACK'
        WHEN avg_annual_growth >= required_annual_growth * 0.8 THEN 'CLOSE'
        ELSE 'BEHIND'
    END as target_status,
    ROUND(current_pct + (avg_annual_growth * years_remaining), 1) as projected_2030_pct
FROM latest_progress
ORDER BY 
    CASE 
        WHEN avg_annual_growth >= required_annual_growth THEN 1
        WHEN avg_annual_growth >= required_annual_growth * 0.8 THEN 2
        ELSE 3
    END,
    gap_to_target;

-- Key insights for dashboard:
-- - "Green leaders": Countries exceeding targets
-- - "At risk": Countries falling behind
-- - Belgium's specific trajectory and ranking
