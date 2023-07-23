import os
import pandas as pd
from apple_store_scraper import AppStore
from google_play_scraper import Sort, reviews_all
import time
from datetime import datetime

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5
FETCH_DELAY_SECONDS = 2

def fetch_with_retry(fetch_function, *args, **kwargs):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            result = fetch_function(*args, **kwargs)
            return result
        except Exception as e:
            if attempt < MAX_RETRIES:
                print(f"Attempt {attempt} failed for {kwargs.get('app_id')} - Retrying in {RETRY_DELAY_SECONDS} seconds...")
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                print(f"Max retries exceeded for {kwargs.get('app_id')} - Error message: {str(e)}")
                return None

def fetch_ios_reviews(country_code, app_name, app_id):
    app = AppStore(country=country_code, app_name=app_name, app_id=app_id)
    app.review(how_many=10000)
    return pd.DataFrame(app.reviews)

def fetch_android_reviews(app_id, country_code):
    result = reviews_all(
        app_id,
        sleep_milliseconds=0,
        lang='en',
        country=country_code,
        sort=Sort.NEWEST,
    )
    return pd.DataFrame(result)

# Load the app information from the CSV file into a DataFrame
app_info_df = pd.read_csv('app_info.csv')

# Get the current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get a set of existing file names (excluding current_date) for duplicate check
existing_file_names = {file_name[:-11] for file_name in os.listdir(current_dir) if file_name.endswith('.csv')}

# Loop through each row in the DataFrame to scrape app reviews
for index, row in app_info_df.iterrows():
    try:
        # Check if the file already exists with the same app information (excluding the date)
        file_exists = any(file_name.startswith(f"{row['country_name']}-{row['brand_name']}-{row['platform']}-reviews-") for file_name in os.listdir('.'))
        if file_exists:
            print(f"File already exists: {file_name} - Skipping fetching for app: {row['app_id']}")
            continue

        # Fetch reviews based on the platform
        if row['platform'] == 'iOS':
            appdf = fetch_with_retry(fetch_ios_reviews, row['country_code'], row['app_name'], row['app_id'])
        elif row['platform'] == 'Android':
            appdf = fetch_with_retry(fetch_android_reviews, row['app_id'], row['country_code'])
        else:
            print(f"Unsupported platform: {row['platform']}")
            continue

        if appdf is None:
            print(f"No reviews found for app: {row['app_id']} - Skipping...")
            continue

        # Get the current date in YYYY-MM-DD format
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Generate the file name with the current date and information from the current row
        file_name = f"{row['country_name']}-{row['brand_name']}-{row['platform']}-reviews-{current_date}.csv"

        # Export the DataFrame to the generated file name if it is not empty
        if not appdf.empty:
            appdf.to_csv(file_name, index=False, encoding='utf-8')
            print(f"Reviews fetched and exported successfully for app: {row['app_id']}")
        else:
            print(f"No reviews found for app: {row['app_id']} - Skipping...")

        # Add a delay between each API call to avoid rate limiting
        time.sleep(FETCH_DELAY_SECONDS)

    except Exception as e:
        print(f"Error fetching reviews for app: {row['app_id']}, Error message: {str(e)}")
        # Optionally, log the error to a file or database for further analysis
        continue

print("All apps processed.")
