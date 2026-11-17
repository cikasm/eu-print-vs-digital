-- How did e-book buying change each year in each country? (2020-2023, same definition)
-- Found: EU average rose from 7.0% (2020) to 8.0% (2023). Malta doubled (5.5% -> 11.1%);
--        Germany fell the most (12.8% -> 8.8%). France has no 2020 value.
SELECT country_code,
       year,
       pct_of_people,
       pct_of_people - LAG(pct_of_people) OVER (
           PARTITION BY country_code ORDER BY year
       ) AS change_from_last_year
FROM mart.fact_book_purchases
WHERE indicator = 'I_BBOOKNLS'
ORDER BY country_code, year;
