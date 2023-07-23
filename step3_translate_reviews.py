from googletrans import Translator
import pandas as pd
import os
import time

# Function to translate the review to English using Google Translate
def translate_to_english(review):
    try:
        # Initialize the translator
        translator = Translator()

        # Translate the review to English
        translation = translator.translate(review, src='auto', dest='en')
        return translation.text

    except Exception as e:
        # If any error occurs during translation, return the original review
        print(f"Error during translation: {str(e)}")
        return review
    
    except Exception as e:
        # If any error occurs during translation, return the original review
        print(f"Error during translation: {str(e)}")
        return review

# Get a list of file names in the current directory
file_names = [file for file in os.listdir('.') if file.endswith('.csv')]

# Loop through each file in the list
for file_name in file_names:
    try:
        # Check if the file name contains 'Android' or 'iOS'
        if 'Android' not in file_name and 'iOS' not in file_name:
            print(f"Skipping file: {file_name} - Unsupported platform.")
            continue

        # Check if the file name already contains 'translated'
        if 'translated' in file_name:
            print(f"Skipping file: {file_name} - Already translated.")
            continue
        
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_name)

        # Check if the DataFrame is empty
        if df.empty:
            print(f"Skipping file: {file_name} - Empty DataFrame.")
            continue

        # Check if the 'review' column exists in the DataFrame
        if 'review' in df.columns:
            print(f"Translating file: {file_name}...")
            # Apply translation to reviews
            df['review'] = df['review'].apply(translate_to_english)

            # Save the translated DataFrame back to the same file, overwriting the original data
            df.to_csv(file_name, index=False, encoding='utf-8')

            # Rename the file by adding 'translated' to the original file name
            translated_file_name = file_name.replace('.csv', '-translated.csv')
            os.rename(file_name, translated_file_name)

            print(f"Translation complete for file: {file_name}")
        else:
            print(f"'review' column not found in file: {file_name}")

    except Exception as e:
        print(f"Error processing file: {file_name}, Error message: {str(e)}")
        continue

    # Add a short delay between API calls to avoid rate limiting
    time.sleep(2)
