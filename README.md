# App Reviews Data Collection and Processing

![Python](https://img.shields.io/badge/python-3.8%2B-blue)

This project contains a collection of Python scripts to fetch, clean, translate, and export app reviews from various platforms, including both iOS and Android apps. The scripts are designed to automate the process of gathering app reviews, making the data analysis and insights more accessible to developers, researchers, and businesses.

## Features

- **Data Collection**: The `step1_fetch_reviews.py` script fetches app reviews from the Apple App Store (iOS) and Google Play Store (Android) using APIs. It supports retry logic to handle potential API errors or timeouts, ensuring robust data collection.

- **Data Cleaning**: The `step2_clean_data.py` script cleans the collected app review data, making it consistent and ready for analysis. It performs text processing tasks such as converting review text to lowercase and removing emojis.

- **Translation (Optional)**: The `step3_translate_reviews.py` script offers optional functionality to translate non-English app reviews to English using Google Translate. This feature provides multilingual insights into user feedback.

- **Data Export**: The `step4_export_file.py` script combines all the cleaned and translated data into a single consolidated file, making it easy to access and analyze the app reviews collectively.

## Requirements

- Python 3.8 or higher
- Required Python libraries are specified in the scripts and include `pandas`, `apple_store_scraper`, `google_play_scraper`, and `googletrans`.

## Installation

1. Clone this GitHub repository to your local machine.
2. Install the required Python libraries using pip:

```bash
pip3 install pandas apple_store_scraper google_play_scraper googletrans==3.1.0-alpha
```

## Usage

**Data Collection**: Execute `step1_fetch_reviews.py` to fetch app reviews from the Apple App Store and Google Play Store. Ensure that the `app_info.csv` file contains the required app information (app_name, app_id, country_code, platform) for the apps you want to fetch reviews for.

**Data Cleaning**: Run `step2_clean_data.py` to clean the fetched reviews data. This script will convert the review text to lowercase and remove emojis.

**Translation (Optional)**: Execute `step3_translate_reviews.py` if you want to translate non-English reviews to English. This script uses Google Translate to perform the translation.

**Data Export**: Run `step4_export_file.py` to combine all cleaned and translated data into a single file. The output file will be named `total_app_reviews_<current_date>.csv`.

## Input File: app_info.csv

The `app_info.csv` file serves as the input to the `step1_fetch_reviews.py` script. This file should be in CSV format and contain the following columns:

- `brand_name`(optional): The name of the brand or company associated with the app.
- `country_code`: The country code (ISO 3166-1 alpha-2 format) where the app is available.
- `country_name` (optional): The full name of the country where the app is available.
- `platform`: The platform of the app (either "iOS" or "Android").
- `app_id`: The unique identifier of the app in the respective app store. For Android, this is the package name, and for iOS, it's the app's ID.
- `app_name`: The name of the app. This field is not required for iOS apps.

An example of the `app_info.csv` file:

```bash
brand_name,country_code,country_name,platform,app_id,app_name
Tortazo,us,United States,Android,com.paytronix.client.android.app.tortazo,Tortazo App
ExampleApp,ca,Canada,iOS,1234567890,Example App
```
Ensure that you have a valid `app_info.csv` file with the required information for the apps you want to fetch reviews for and place it in the appropriate location where the Python scripts can access it.

## App Store Reviews and Ratings

1. **Weighted Ratings on Google Play**: Google Play gives more weight to the ratings from the latest app versions. That way, it wants to reward app developers and marketers for their improvement. So the average app rating for Android apps is more influenced by recent ratings than those given a few years ago.

2. **Variations in Ratings Across Territories**: An app can receive different ratings in different territories due to variations in rating standards across different regions. Each rating authority applies its criteria when rating apps, which may result in differences in ratings across territories.

3. **Discrepancy in Review Count**: The number of written reviews fetched might be less than the total number of ratings displayed. This discrepancy is due to the fact that not all the users who rated the app also provide written reviews. 

It's essential to consider these factors when analyzing and interpreting app reviews and ratings to gain a comprehensive understanding of user feedback and app performance across different platforms and regions.

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute the code as per the terms of the license.

## Acknowledgments

- The [`apple_store_scraper`](https://pypi.org/project/apple-store-scraper/) and [`google_play_scraper`](https://pypi.org/project/google-play-scraper/) libraries are used to access the Apple App Store and Google Play Store APIs, respectively.
- The `googletrans` library provides the translation functionality using the Google Translate service.

## Contributing

We welcome contributions to improve the project. If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.
