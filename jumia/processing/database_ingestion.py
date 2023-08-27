import os
import mysql.connector
from dotenv import load_dotenv
from normalization import normalize_dataset
from file_reader import object_loader
# from pandas_processor import process_data



# Load environment variables from .env file
#dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
#load_dotenv(dotenv_path)

# Dataset file is named 'dataset.json' and located in the 'data' directory
file_path = '../dataset/extracted/jumiascraper_2023-06-21T23-49-42.json'

# Load the dataset from the JSON file
dataset = object_loader(file_path)

# Normalize the dataset
normalized_dataset = normalize_dataset(dataset)
 

# Connect to the MySQL database

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Kanwaldotuniv1!",
    "database": "jumia_db"
}


conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Open a cursor to perform database operations
try:
    # # Insert the normalized data into the MySQL table
    for item in normalized_dataset:
        query = "INSERT INTO mobile_phones (crawled_at, item_url, data_id, brand, specs, price, old_price, discount, votes, stars, image_url, official_store) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            item['crawled_at'],
            item['item_url'],
            item['data_id'],
            item['brand'],
            item['specs'],
            item['price'],
            item['old_price'],
            item['discount'],
            item['votes'],
            item['stars'],
            item['image_url'],
            item['official_store']
        )
        cursor.execute(query, values)

except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
else:
    print("Data inserted successfully")
    conn.commit()
finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()
