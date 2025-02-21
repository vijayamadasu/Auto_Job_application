import pandas as pd

# Define job details for the new job posting
job_data = {
    "Title": ["Junior Quality Assurance (m/f/d)"],
    "Company": ["TeleClinic"],
    "Location": ["Germany"],
    "Link": ["https://www.teleclinic.com/karriere/junior-quality-assurance-m-f-d/"]
}

# Create DataFrame
job_df = pd.DataFrame(job_data)

# Save to CSV file
csv_filename = "company_jobs.csv"
job_df.to_csv(csv_filename, index=False)

print(f"CSV file '{csv_filename}' has been created successfully!")
