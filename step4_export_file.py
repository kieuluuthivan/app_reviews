import pandas as pd
import os
from googletrans import Translator
import unicodedata
from datetime import datetime

# Get a list of file names in the current directory
file_names = [file for file in os.listdir('.') if file.endswith('-translated.csv')]

# Initialize an empty list to store all the dataframes
dfs = []

# Loop through each file in the list
for file_name in file_names:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_name)
    
    # Get platform, brand, and country from the file name
    file_parts = file_name[:-15].split('-')  # Remove the "-translated.csv" extension
    platform = file_parts[2]
    brand = file_parts[1]
    country = file_parts[0]
    
    # Add new columns for platform, brand, and country
    df['platform'] = platform
    df['brand'] = brand
    df['country'] = country
    
    # Extract only the required columns
    df = df[['date', 'review', 'rating', 'platform', 'brand', 'country']]
    
    # Append the dataframe to the list
    dfs.append(df)

# Concatenate all dataframes in the list into a single dataframe
combined_df = pd.concat(dfs, ignore_index=True)

# Get the current date in YYYY-MM-DD format
current_date = datetime.now().strftime('%Y-%m-%d')

# Update the final file name to include the current date
combined_file_name = f'total_app_reviews_{current_date}.csv'

# Save the combined dataframe to the new file
combined_df.to_csv(combined_file_name, index=False, encoding='utf-8')

print(f"All files combined and saved to {combined_file_name}.")
