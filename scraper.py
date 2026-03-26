import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def scrape_rozee_jobs():
    # 1️⃣ Setup Selenium WebDriver
    # Provide path to chromedriver executable
    service = Service("C:/chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    # 2️⃣ URL of the Rozee.pk Data Engineer job search page
    url = "https://www.rozee.pk/job/jsearch/q/Data%20Engineer/fc/1185/stype/title"
    driver.get(url)  # Open the page in Chrome

    jobs = []  # List to store scraped job data
    page = 1  # Pagination counter

    # 3️⃣ Loop through all pages
    while True:
        print(f"Scraping page {page}...")
        time.sleep(4)  # Wait for page to fully load (important for dynamic JS content)

        # 4️⃣ Select all job cards on the page
        job_cards = driver.find_elements(By.CSS_SELECTOR, "div.job")

        # 5️⃣ Loop through each job card and extract information
        for job in job_cards:
            # Job Title
            try:
                title = job.find_element(By.TAG_NAME, "a").text
            except:
                title = "N/A"

            # Company Name
            try:
                company = job.find_element(By.CSS_SELECTOR, ".company").text
            except:
                company = "N/A"

            # Location
            try:
                location = job.find_element(By.CSS_SELECTOR, ".location").text
            except:
                location = "N/A"

            # Job Link (URL)
            try:
                link = job.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                link = "N/A"

            # Skills (comma-separated string if multiple)
            try:
                skills_tag = job.find_element(
                    By.CSS_SELECTOR,
                    ".skills",  # The CSS selector for skills; may need adjustment if site changes
                )
                skills = skills_tag.text.strip()
            except:
                skills = "N/A"

            # Append scraped data to jobs list
            jobs.append(
                {
                    "job_title": title,
                    "company": company,
                    "location": location,
                    "job_link": link,
                    "skills": skills,
                    "scrape_date": datetime.today().date(),  # Record the date of scraping
                }
            )

        # 6️⃣ Pagination: Click "Next" if available
        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next")
            next_button.click()  # Go to next page
            page += 1
        except:
            print("No more pages.")  # Exit loop if no more pages
            break

    # 7️⃣ Close browser after scraping
    driver.quit()

    # 8️⃣ Save all scraped jobs to CSV
    df = pd.DataFrame(jobs)
    df.to_csv("raw_jobs.csv", index=False)

    print("Total jobs scraped:", len(df))


if __name__ == "__main__":
    scrape_rozee_jobs()
