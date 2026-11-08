/* ============================================================
   Energy Price Pulse: analysis views
   Each view feeds one part of the Power BI dashboard.
   Run after 01_create_tables.sql.
   ============================================================ */

/* ---------- 1. Gasoline vs. 13-week moving average ---------- */
CREATE VIEW gasoline_moving_avg AS
SELECT
    price_date,
    price,
    AVG(price) OVER (ORDER BY price_date
                     ROWS BETWEEN 12 PRECEDING AND CURRENT ROW) AS moving_avg_13wk
FROM gasoline_weekly;


/* ---------- 2. Electricity vs. 3-month moving average ---------- */
CREATE VIEW electricity_moving_avg AS
SELECT
    price_month,
    price,
    AVG(price) OVER (ORDER BY price_month
                     ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_3mo
FROM electricity_monthly;


/* ---------- 3. Natural gas vs. 3-month moving average ---------- */
CREATE natural_gas_moving_avg AS
SELECT
    price_month,
    price,
    AVG(price) OVER (ORDER BY price_month
                     ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_3mo
FROM natural_gas_monthly;
GO

/* ---------- 4. Average price by year (all three fuels) ---------- */
CREATE VIEW vw_avg_price_by_year AS
SELECT 'Gasoline' AS fuel, YEAR(price_date) AS price_year,
       CAST(AVG(price) AS DECIMAL(6,2)) AS avg_price, '$/gal' AS unit
FROM gasoline_weekly
GROUP BY YEAR(price_date)
UNION ALL
SELECT 'Electricity', YEAR(price_month),
       CAST(AVG(price) AS DECIMAL(6,2)), 'cents/kWh'
FROM electricity_monthly
GROUP BY YEAR(price_month)
UNION ALL
SELECT 'Natural Gas', YEAR(price_month),
       CAST(AVG(price) AS DECIMAL(6,2)), '$/MCF'
FROM natural_gas_monthly
GROUP BY YEAR(price_month);
GO

/* ---------- 5. KPI cards: latest price and year-over-year % change ---------- */
ALTER VIEW kpi_latest AS
WITH gas AS (
    SELECT TOP 1 g.price_date AS latest_period, g.price AS latest_price,
           (SELECT TOP 1 p.price FROM gasoline_weekly p
            WHERE p.price_date <= DATEADD(WEEK, -52, g.price_date)
            ORDER BY p.price_date DESC) AS price_1yr_ago
    FROM gasoline_weekly g
    ORDER BY g.price_date DESC
),
elec AS (
    SELECT TOP 1 e.price_month AS latest_period, e.price AS latest_price,
           (SELECT p.price FROM electricity_monthly p
            WHERE p.price_month = DATEADD(YEAR, -1, e.price_month)) AS price_1yr_ago
    FROM electricity_monthly e
    ORDER BY e.price_month DESC
),
ng AS (
    SELECT TOP 1 n.price_month AS latest_period, n.price AS latest_price,
           (SELECT p.price FROM natural_gas_monthly p
            WHERE p.price_month = DATEADD(YEAR, -1, n.price_month)) AS price_1yr_ago
    FROM natural_gas_monthly n
    ORDER BY n.price_month DESC
)
SELECT 'Gasoline' AS fuel, latest_period, latest_price, price_1yr_ago,
       CAST((latest_price - price_1yr_ago) * 100.0 / price_1yr_ago AS DECIMAL(6,2)) AS yoy_pct_change
FROM gas
UNION ALL
SELECT 'Electricity', latest_period, latest_price, price_1yr_ago,
       CAST((latest_price - price_1yr_ago) * 100.0 / price_1yr_ago AS DECIMAL(6,2))
FROM elec
UNION ALL
SELECT 'Natural Gas', latest_period, latest_price, price_1yr_ago,
       CAST((latest_price - price_1yr_ago) * 100.0 / price_1yr_ago AS DECIMAL(6,2))
FROM ng;
GO




/* ---------- 6. Shock window: monthly % change, 2026 vs. same month 2025 ---------- */
ALTER VIEW 2026_shock_comparison AS
SELECT
    'Gasoline' AS fuel,
    DATEFROMPARTS(YEAR(price_date), MONTH(price_date), 1) AS price_month,
    CAST(AVG(price) AS DECIMAL(6,3)) AS avg_price
FROM gasoline_weekly
WHERE YEAR(price_date) IN (2025, 2026)
GROUP BY DATEFROMPARTS(YEAR(price_date), MONTH(price_date), 1)
UNION ALL
SELECT 'Electricity', price_month, price FROM electricity_monthly WHERE YEAR(price_month) IN (2025, 2026)
UNION ALL
SELECT 'Natural Gas', price_month, price FROM natural_gas_monthly WHERE YEAR(price_month) IN (2025, 2026);
GO







SELECT * 
FROM gasoline_weekly
