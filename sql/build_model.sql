-- A separate area for the finished, analysis-ready tables
CREATE SCHEMA IF NOT EXISTS mart;

-- DIMENSION: countries
-- Grain: one row = one EU country
DROP TABLE IF EXISTS mart.dim_country;
CREATE TABLE mart.dim_country AS
SELECT country_code, country_name, region, euro_member
FROM staging.countries;

-- FACT: online book purchases
-- Grain: one row = one country, one year, one indicator
DROP TABLE IF EXISTS mart.fact_book_purchases;
CREATE TABLE mart.fact_book_purchases AS
SELECT country_code,
       year,
       indicator,
       indicator_label,
       CASE WHEN indicator = 'I_BBOOKNLG' THEN 'print' ELSE 'digital' END AS format,
       value AS pct_of_people,
       flag
FROM staging.book_purchases;

-- FACT: books read in the last 12 months (survey, 2022 only)
-- Grain: one row = one country, one year, one sex, one age group, one "books read" group
DROP TABLE IF EXISTS mart.fact_reading;
CREATE TABLE mart.fact_reading AS
SELECT country_code,
       year,
       sex,
       age,
       books_read,
       books_read_label,
       value AS pct_of_people,
       flag
FROM staging.reading;

-- FACT: Google search interest
-- Grain: one row = one country, one week, one keyword
DROP TABLE IF EXISTS mart.fact_search_interest;
CREATE TABLE mart.fact_search_interest AS
SELECT country_code,
       CAST(date AS date) AS week_start,
       keyword,
       format,
       interest
FROM staging.trends;
