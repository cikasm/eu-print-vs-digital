-- Do countries where more people read also buy more e-books? (2022, the only survey year)
-- Found: Yes, strongly (correlation 0.75 across 26 countries; no German survey data).
--        Luxembourg and Denmark read the most; Romania (29%) and Cyprus (33%) the least.
WITH readers AS (
    SELECT country_code,
           ROUND((100 - pct_of_people)::numeric, 1) AS pct_read_any_book   -- everyone except "no books"
    FROM mart.fact_reading
    WHERE year = 2022 AND sex = 'T' AND age = 'Y_GE16' AND books_read = '0'
),
ebooks AS (
    SELECT country_code, pct_of_people AS pct_bought_ebooks
    FROM mart.fact_book_purchases
    WHERE year = 2022 AND indicator = 'I_BBOOKNLS'
)
SELECT d.country_name,
       r.pct_read_any_book,
       e.pct_bought_ebooks,
       ROUND(CORR(r.pct_read_any_book, e.pct_bought_ebooks) OVER ()::numeric, 2) AS correlation
FROM readers r
JOIN ebooks e ON e.country_code = r.country_code
JOIN mart.dim_country d ON d.country_code = r.country_code
ORDER BY r.pct_read_any_book DESC;
