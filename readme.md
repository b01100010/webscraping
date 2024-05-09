# Automate web Scraping, ELT pipeline 

This project will scraper the data from seek.com.au for the job available within 25km range from Sydney CBD. The script will be triggered hourly and write the data to Google Cloud Storage.

## Project plan
1. Scrape the data from the data source.
2. Write data into JSON file and upload to Google Cloud Storage to serve as data warehouse.
3. Load data into Google Bigquery
