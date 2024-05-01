from selenium.webdriver import Chrome, ChromeOptions
import json

from datetime import datetime

from google.cloud import storage

# //span[@data-automation="totalJobsCount"] return job count
# //span[@data-automation="item-text"] return job classification name
# //span[@data-automation="item-count"] return job count by classification

def upload_to_gcs(bucket_name, destination_blob_name, credentials_file, json_object):
    # Initialize the Google Cloud Storage client with the credentials
    storage_client = storage.Client.from_service_account_json(credentials_file)

    # Get the target bucket
    bucket = storage_client.bucket(bucket_name)

    # Upload the file to the bucket
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(data=json.dumps(json_object), content_type='application/json')

    print(f"File uploaded to gs://{bucket_name}/{destination_blob_name}")

def get_data(url):
    options = ChromeOptions()
    options.add_argument("--headless=new")

    driver = Chrome(options=options)
    driver.get(url)

    job_count = driver.find_element("xpath", '//span[@data-automation="totalJobsCount"]').text.replace(',','')
    total_job = dict(total_posted = int(job_count))

    job_class_names = driver.find_elements("xpath",'//span[@data-automation="item-text"]')
    job_class_counts = driver.find_elements("xpath",'//span[@data-automation="item-count"]')
    
    job_posted = {}
    for name, count in zip(job_class_names,job_class_counts):
        job_name = name.get_attribute('textContent').replace('&', 'and').replace(',', 'or').replace(' ','_')
        count_total = count.get_attribute('textContent')

        job_posted[job_name] = int(count_total)
        
    driver.quit()

    curr_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    timestamp = dict(posted_time = curr_date)

    data = {
    "total_posted": total_job["total_posted"],
    "categories": job_posted,
    "posted_time": timestamp["posted_time"]
    }

    return data

def main():
    url = 'https://www.seek.com.au/jobs/in-Sydney-NSW-2000?daterange=1&distance=25'
    data = get_data(url)

    time = datetime.now().strftime('%H:%M')
    filename = f"seek_data_{time}.json"

    day = datetime.now().strftime('%Y-%m-%d')

    GS_PROJECT_ID = 'seekWebScraper'
    BUCKET_NAME = "seek62"
    DESTINATION_BLOB_NAME = f'sydney/{day}/{filename}'
    CREDENTIALS_FILE = "/Users/beeboossadee/Downloads/credentials.json"

    upload_to_gcs(BUCKET_NAME, DESTINATION_BLOB_NAME, CREDENTIALS_FILE, data)

if __name__ == '__main__':
    main()





