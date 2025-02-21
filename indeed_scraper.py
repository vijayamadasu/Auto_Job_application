from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

# Indeed Job Search URL (Germany, Data Scientist)
job_search_url = "https://de.indeed.com/jobs?q=data+scientist&l=Germany"
driver.get(job_search_url)
time.sleep(random.uniform(5, 8))  # Random wait time to avoid detection

# Wait for user to manually solve CAPTCHA if needed
input("If CAPTCHA appears, solve it and press Enter to continue...")

# Scrape job postings
jobs = []
for _ in range(3):  # Scroll multiple times to load more jobs
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(5, 8))  # Increased random wait time to mimic human behavior

# Extract job elements
soup = BeautifulSoup(driver.page_source, "html.parser")
job_listings = soup.find_all("div", class_="job_seen_beacon")  # Class may change, inspect manually

print(f"Total job listings found in HTML: {len(job_listings)}")

for job in job_listings:
    try:
        title = job.find("h2", class_="jobTitle").text.strip()
        company = job.find("span", class_="companyName").text.strip()
        location = job.find("div", class_="companyLocation").text.strip()
        job_link = "https://de.indeed.com" + job.find("a", class_="jcs-JobTitle")['href']
        
        jobs.append({
            "Title": title,
            "Company": company,
            "Location": location,
            "Link": job_link
        })
    except Exception as e:
        print(f"Error extracting job details: {e}")
        continue

print(f"Total jobs scraped: {len(jobs)}")

# Convert to DataFrame and Save
job_df = pd.DataFrame(jobs)
if job_df.empty:
    print("No jobs found! Check the website structure.")
else:
    job_df.to_csv("indeed_jobs.csv", index=False)
    print("Scraping Completed. Data saved as 'indeed_jobs.csv'")

# Keep browser open for inspection
input("Press Enter to close the browser...")

# Close the driver
driver.quit()
