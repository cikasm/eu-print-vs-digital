-- How has Google search interest in each keyword changed per year? (10 countries, full years 2022-2025)
-- Found: Kindle searches rose every year (avg 28 -> 38), bullet journal faded (4.3 -> 1.4),
--        planner was flat (~31-34). "notebook" also means laptop in many languages, so read it with care.
-- Note: Trends scores are 0-100 relative within each country, so we compare change, not levels.
SELECT keyword,
       format,
       EXTRACT(YEAR FROM week_start)::int AS year,
       ROUND(AVG(interest)::numeric, 1) AS avg_interest
FROM mart.fact_search_interest
WHERE EXTRACT(YEAR FROM week_start) BETWEEN 2022 AND 2025
GROUP BY keyword, format, year
ORDER BY keyword, year;
