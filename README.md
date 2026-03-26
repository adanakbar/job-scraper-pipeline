# Job Scraping Pipeline

A complete **end-to-end data pipeline** that scrapes **Data Engineer jobs** from [Rozee.pk](https://www.rozee.pk), processes the data, and loads it into a **SQL Server data warehouse (Star Schema)** for analytics.
## Project Overview
This project demonstrates a real-world **data engineering workflow**:
Rozee.pk (Dynamic Website)
↓
Selenium Scraper
↓
Raw CSV (raw_jobs.csv)
↓
Pandas Transformation
↓
SQL Server (Star Schema)

## Tech Stack
- **Python**
- **Selenium** (Web Scraping)
- **Pandas** (Data Transformation)
- **SQL Server** (Data Warehouse)
- **ODBC / pyodbc** (Database Connection)

## Project Structure
- job-scraper-pipeline/
- scraper.py # Scrapes job data using Selenium
- transform.py # Cleans and transforms raw data 
- load.py # Loads data into SQL Server
- requirements.txt # Dependencies
- README.md # Documentation

## Important Notes
-💡 Ensure that the ChromeDriver version matches your installed Chrome browser.
- The scraper handles dynamic content and pagination.
- Missing skills are handled gracefully (skipped if not available).


