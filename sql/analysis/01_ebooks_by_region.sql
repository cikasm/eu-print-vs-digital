-- Which EU regions buy the most e-books online? (2023)
-- Found: Nordic countries lead (16.7% of people bought e-books online), then Western (12.7%);
--        Southern (4.7%) and Central-Eastern (4.4%) are far behind.
SELECT d.region,
       ROUND(AVG(f.pct_of_people)::numeric, 1) AS avg_pct
FROM mart.fact_book_purchases f
JOIN mart.dim_country d ON f.country_code = d.country_code
WHERE f.indicator = 'I_BBOOKNLS'   -- digital: e-books, online magazines/newspapers (until 2023)
  AND f.year = 2023
GROUP BY d.region
ORDER BY avg_pct DESC;
