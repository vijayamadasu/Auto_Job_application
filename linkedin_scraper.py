from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from bs4 import BeautifulSoup

# Setup Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

# Initialize Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# LinkedIn Login Credentials
LINKEDIN_EMAIL = "vijayamadasu1@gmail.com"
LINKEDIN_PASSWORD = "Vijaya@123"

# Open LinkedIn and Login
driver.get("https://www.linkedin.com/login")
time.sleep(3)

driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
time.sleep(5)

# Verify successful login
if "feed" not in driver.current_url:
    print("Login failed! Check credentials or CAPTCHA requirement.")
    driver.quit()
    exit()

# Navigate to LinkedIn Jobs Search Page
job_search_url = "https://www.linkedin.com/jobs/search/?keywords=data%20scientist&location=Germany"
driver.get(job_search_url)

# Wait for job listings to load




try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results__list-item"))
    )
    print("Job listings loaded successfully.")
except:
    print("Timeout: Job listings did not load in time.")
    driver.quit()
    exit()


time.sleep(5)

# Scrape job postings
jobs = []
for _ in range(3):  # Scroll multiple times to load more jobs
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Increased wait time for dynamic loading

# Extract job elements
soup = BeautifulSoup(driver.page_source, "html.parser")
job_listings = soup.find_all("div", class_="t-24 job-details-jobs-unified-top-card__job-title")

print(f"Total job listings found in HTML: {len(job_listings)}")  # Debugging

for job in job_listings:
    try:
        title = job.find("span", class_="sr-only").text.strip()
        company = job.find("span", class_="job-card-container__company-name").text.strip()
        location = job.find("span", class_="job-card-container__metadata-item").text.strip()
        job_link = job.find("a", class_="job-card-container__link")["href"].strip()
        
        jobs.append({
            "Title": title,
            "Company": company,
            "Location": location,
            "Link": job_link
        })
    except Exception as e:
        print(f"Error extracting job details: {e}")
        continue

print(f"Total jobs scraped: {len(jobs)}")  # Debugging

# Convert to DataFrame and Save
job_df = pd.DataFrame(jobs)
if job_df.empty:
    print("No jobs found! Check the website structure or login session.")
else:
    job_df.to_csv("linkedin_jobs.csv", index=False)
    print("Scraping Completed. Data saved as 'linkedin_jobs.csv'")

# Close the driver
driver.quit()
