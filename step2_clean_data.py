import pandas as pd
from datetime import datetime
import re
import os

def clean_reviews(df):
    # Clean the review text by making it consistent (lowercase) and removing emojis
    df['review'] = df['review'].fillna('').apply(lambda x: re.sub(r'[^\w\s]', '', x.lower()))
    return df

def clean_android_reviews(df):
    # Check if the 'at' column exists in the DataFrame
    if 'at' not in df.columns:
        print(f"Error: 'at' column not found in file.")
        return df

    # Rename the "at" column to "date" and convert the date format
    df['date'] = pd.to_datetime(df['at']).dt.strftime('%Y-%m-%d')
    df.drop(columns=['at'], inplace=True)  # Remove the original "at" column

    # Rename the "score" column to "rating"
    df.rename(columns={'score': 'rating'}, inplace=True)

    # Rename the "content" column to "review"
    df.rename(columns={'content': 'review'}, inplace=True)

    return clean_reviews(df)

# Get the current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))

# List all CSV files in the directory
csv_files = [file for file in os.listdir(current_dir) if file.endswith('.csv')]

for file_name in csv_files:
    # You can check if the platform name 'Android' is in the file name
    if 'Android' in file_name:
        platform = 'android'
    elif 'iOS' in file_name:
        platform = 'ios'
    else:
        print(f"Unsupported platform. Skipping file: {file_name}")
        continue

    # Load the CSV file into a DataFrame
    try:
        df = pd.read_csv(file_name)
    except pd.errors.EmptyDataError:
        print(f"Error: Empty DataFrame in file: {file_name}")
        continue

    if df.empty:
        print(f"Error: Empty DataFrame in file: {file_name}")
        continue

    if platform == 'android':
        # Apply the cleaning logic for Android reviews
        df = clean_android_reviews(df)
    elif platform == 'ios':
        # For iOS reviews, we don't need to perform any specific cleaning, but we'll apply the common cleaning
        # (converting review text to lowercase and removing emojis) for both platforms
        df = clean_reviews(df)
    else:
        print(f"Unsupported platform: {platform} - Skipping file: {file_name}")
        continue

    # Save the cleaned DataFrame back to the same file, overwriting the original data
    df.to_csv(file_name, index=False, encoding='utf-8')

print("All files processed.")
