-- In which countries do online book buyers lean digital rather than print? (2023)
-- Found: Print still wins almost everywhere. Only Finland (60% digital share) and
--        Denmark (55%) lean digital; Portugal (21%) and Italy (24%) lean most to print.
SELECT d.country_name,
       d.region,
       p.pct_of_people AS print_pct,
       e.pct_of_people AS digital_pct,
       ROUND((100 * e.pct_of_people / NULLIF(p.pct_of_people + e.pct_of_people, 0))::numeric, 1)
           AS digital_share_pct
FROM mart.fact_book_purchases p
JOIN mart.fact_book_purchases e
  ON e.country_code = p.country_code AND e.year = p.year AND e.indicator = 'I_BBOOKNLS'
JOIN mart.dim_country d ON d.country_code = p.country_code
WHERE p.indicator = 'I_BBOOKNLG'
  AND p.year = 2023
ORDER BY digital_share_pct DESC;
