# U.S. Energy Price Shock Analysis

How fast do energy prices react to a geopolitical shock? This project pulls U.S. gasoline, electricity, and natural gas prices from the U.S. Energy Information Administration (EIA), models them in SQL Server, and visualizes them in an interactive Power BI dashboard built around the 2026 Iran conflict.

![Dashboard overview](screenshots/dashboard_overview.png)

## Key Finding

**Gasoline prices reacted almost immediately to the 2026 Iran conflict, while residential electricity and natural gas prices moved gradually.**

- Gasoline is reported **weekly**, so the shock shows up within days.
- Electricity and natural gas are reported **monthly**, and retail prices also lag because of utility contracts and rate regulation.
- Takeaway: both **data frequency** and **market structure** decide how quickly a price shock becomes visible. Analysts comparing these series have to account for that before drawing conclusions.

## Tools

| Stage | Tool |
|---|---|
| Data extraction | Python (`requests`, `pandas`) via the EIA API v2 |
| Cleaning & filtering | Python (`pandas`), Excel |
| Data modeling & queries | SQL Server (SSMS) |
| Visualization | Power BI |

## Pipeline

```
EIA API  →  Python (pull + filter)  →  Excel  →  SQL Server  →  Power BI
```

1. **Extract:** Python scripts call the EIA API for weekly retail gasoline prices, plus monthly residential electricity and residential natural gas prices.
2. **Clean:** pandas filters the series, standardizes dates and units, and exports clean files.
3. **Model:** The data is loaded into SQL Server, where queries align weekly and monthly series and calculate price changes over time.
4. **Visualize:** Power BI connects to SQL Server for the trend lines, KPI cards, and before/after comparisons around the conflict.

## Repository Contents

| Folder / File | What's inside |
|---|---|
| `python/` | API extraction and cleaning scripts |
| `sql/` | Table setup and analysis queries |
| `powerbi/` | Power BI dashboard file (`.pbix`) |
| `screenshots/` | Dashboard images |

## How to Run

1. Get a free API key at [eia.gov/opendata](https://www.eia.gov/opendata/).
2. In the Python script, replace `YOUR_KEY_HERE` with your key. **Never commit a real key.**
3. Install dependencies: `pip install requests pandas`
4. Run the extraction script, then load the output into SQL Server and run the queries in `sql/`.
5. Open the `.pbix` file in Power BI Desktop and point the data source to your SQL Server instance.

## Author

**Carl D. Pericles**: Marine Corps veteran and data analytics student (B.A.S., Data Analytics & AI, Broward College)
[LinkedIn](https://www.linkedin.com/in/carlpericles) · [GitHub](https://github.com/CarlPericles18)
