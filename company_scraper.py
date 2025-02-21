from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import random
from bs4 import BeautifulSoup

# Setup Chrome options
chrome_options = Options()
# Disable headless mode to see the browser
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Makes Selenium less detectable
chrome_options.add_argument("--incognito")  # Run in incognito mode
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

# Initialize Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# List of company career pages to scrape
company_urls = [
    "https://www.example-company1.com/careers/jobs",
    "https://www.example-company2.com/careers/open-positions"
]

all_jobs = []

for company_url in company_urls:
    print(f"Scraping: {company_url}")
    driver.get(company_url)
    time.sleep(random.uniform(5, 8))  # Random wait time

    # Extract job elements
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_listings = soup.find_all("div", class_="job-listing")  # Update this class based on company site

    print(f"Total job listings found: {len(job_listings)}")

    for job in job_listings:
        try:
            title = job.find("h2").text.strip()
            company = "Company Name"  # Update if needed
            location = job.find("span", class_="job-location").text.strip()
            job_link = job.find("a", href=True)['href']
            
            all_jobs.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Link": job_link
            })
        except Exception as e:
            print(f"Error extracting job details: {e}")
            continue

# Convert to DataFrame and Save
job_df = pd.DataFrame(all_jobs)
if job_df.empty:
    print("No jobs found! Check the website structures.")
else:
    job_df.to_csv("company_jobs.csv", index=False)
    print("Scraping Completed. Data saved as 'company_jobs.csv'")

# Keep browser open for inspection
input("Press Enter to close the browser...")

# Close the driver
driver.quit()
