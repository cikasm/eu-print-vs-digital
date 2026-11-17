# Project notes

## Data source
Eurostat dataset `isoc_ec_ibgs`: Internet purchases, goods or services (2020 onwards).
Values = % of people who bought this online in the last 3 months.

## Indicator codes (`indic_is`)

| Code | Meaning | Years | Format |
|---|---|---|---|
| `I_BBOOKNLG` | Printed books, magazines or newspapers | 2020–2024 | print |
| `I_BBOOKNLS` | E-books, online magazines or online newspapers | 2020–2023 | digital |
| `I_BBOOK2` | E-books or audiobooks as downloads | 2024–2025 | digital |
| `I_BBOOKNLS2` | Paid subscriptions to online news, e-papers or online magazines | 2024–2025 | digital |

**Main codes for print vs e-books:** `I_BBOOKNLG` (print) vs `I_BBOOKNLS` (until 2023) / `I_BBOOK2` (from 2024).

## Other useful codes
- `ind_type` = `IND_TOTAL`: all individuals (use this for headline numbers)
- `unit` = `PC_IND`: percentage of all individuals

## Flags (`flag` column)
- `u`: low reliability
- `b`: break in time series
- `e`: estimated
- `bu`: break in time series, low reliability

## Watch out
- Digital definitions changed in 2024, so 2023 → 2024 is not a like-for-like comparison.
- No country has print data for 2025 (yet).
- Measures online purchases, not reading. Print bought in shops or borrowed from libraries is not counted.
