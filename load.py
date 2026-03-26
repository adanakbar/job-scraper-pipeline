import pandas as pd
import pyodbc
from datetime import datetime


def load_jobs_to_sql():
    # 1️⃣ Connect to SQL Server
    # Using pyodbc to connect to local SQL Server instance
    conn = pyodbc.connect(
        r"Driver={SQL Server};"  # Using SQL Server ODBC driver
        r"Server=ACERASPIRE5\SQLEXPRESS01;"  # Server name (your local SQL Express instance)
        r"Database=job_pipeline;"  # Target database
        r"Trusted_Connection=yes;"  # Windows Authentication
    )
    cursor = conn.cursor()  # Cursor object to execute SQL commands

    # 2️⃣ Read the CSV
    # Load the scraped jobs CSV into a pandas DataFrame
    df = pd.read_csv("raw_jobs.csv")

    # 3️⃣ Ensure scrape_date is standardized
    # Convert scrape_date column to datetime, then format as string YYYY-MM-DD
    df["scrape_date"] = pd.to_datetime(df["scrape_date"], errors="coerce").dt.strftime(
        "%Y-%m-%d"
    )

    # 4️⃣ Loop through each row/job in the CSV
    for index, row in df.iterrows():
        # Extract job attributes, handling missing values
        company_name = row["company"] if pd.notnull(row["company"]) else "N/A"
        job_title = row["job_title"] if pd.notnull(row["job_title"]) else "N/A"
        location = row["location"] if pd.notnull(row["location"]) else "N/A"
        job_link = row["job_link"] if pd.notnull(row["job_link"]) else "N/A"
        scrape_date = row["scrape_date"]  # already formatted as string

        # ---- DIM COMPANY ----
        # Check if company already exists in dim_company
        cursor.execute(
            "SELECT company_id FROM dim_company WHERE company_name = ?", company_name
        )
        result = cursor.fetchone()
        if result:
            company_id = result[0]  # Use existing company_id
        else:
            # Insert new company and retrieve its ID
            cursor.execute(
                "INSERT INTO dim_company (company_name) VALUES (?)", company_name
            )
            cursor.execute(
                "SELECT company_id FROM dim_company WHERE company_name = ?",
                company_name,
            )
            company_id = cursor.fetchone()[0]

        # ---- FACT JOBS ----
        # Check if job already exists in fact_jobs by job_link
        cursor.execute("SELECT job_id FROM fact_jobs WHERE job_link = ?", job_link)
        result = cursor.fetchone()
        if not result:
            # Insert new job if it doesn't exist
            cursor.execute(
                """
                INSERT INTO fact_jobs (job_title, company_id, job_link, scrape_date)
                VALUES (?, ?, ?, ?)
            """,
                job_title,
                company_id,
                job_link,
                scrape_date,
            )
            # Retrieve the generated job_id
            cursor.execute("SELECT job_id FROM fact_jobs WHERE job_link = ?", job_link)
            job_id = cursor.fetchone()[0]
        else:
            job_id = result[0]  # Use existing job_id

        # ---- DIM SKILLS & JOB_SKILLS ----
        # Prepare skills list from CSV (assumes comma-separated skills in a column named 'skills')
        skills_list = []
        if "skills" in row and pd.notnull(row["skills"]):
            # Split skills by comma, remove whitespace, capitalize
            skills_list = [
                s.strip().title() for s in str(row["skills"]).split(",") if s.strip()
            ]

        # Insert skills and populate bridge table
        for skill in skills_list:
            # Check if skill already exists in dim_skills
            cursor.execute(
                "SELECT skill_id FROM dim_skills WHERE skill_name = ?", skill
            )
            result = cursor.fetchone()
            if result:
                skill_id = result[0]  # Use existing skill_id
            else:
                # Insert new skill
                cursor.execute("INSERT INTO dim_skills (skill_name) VALUES (?)", skill)
                cursor.execute(
                    "SELECT skill_id FROM dim_skills WHERE skill_name = ?", skill
                )
                skill_id = cursor.fetchone()[0]

            # Insert into bridge table if this job-skill combination doesn't exist
            cursor.execute(
                """
                IF NOT EXISTS (SELECT 1 FROM job_skills WHERE job_id = ? AND skill_id = ?)
                INSERT INTO job_skills (job_id, skill_id) VALUES (?, ?)
            """,
                job_id,
                skill_id,
                job_id,
                skill_id,
            )

    # ---- COMMIT & CLOSE CONNECTION ----
    # Save all changes to database
    conn.commit()
    # Close cursor and connection
    cursor.close()
    conn.close()

    print(f"Loaded {len(df)} jobs and associated skills into SQL Server.")


if __name__ == "__main__":
    load_jobs_to_sql()
