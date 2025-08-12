import pandas as pd
import numpy as np
import logging
import json
from sensor.config import mongo_client


def dump_csv_file_to_mongodb(file_path:str, database_name:str, collection_name:str) -> None:
    try:
        # Read CSV file into DataFrame
        df = pd.read_csv(file_path)
        df.reset_index(drop=True, inplace=True)

        # Convert DataFrame to list of dictionaries (row-wise records)
        json_records = df.to_dict(orient="records")

        # Insert records into MongoDB
        mongo_client[database_name][collection_name].insert_many(json_records)
        print("File uploaded successfully!")

    except Exception as e:
        print (e)