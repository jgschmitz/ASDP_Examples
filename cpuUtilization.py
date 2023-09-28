#This will send an email alert once utilization hits 70%

from pymongo import MongoClient
import numpy as np

# Connect to MongoDB on localhost (default host and port)
client = MongoClient("localhost", 27017)  # 27017 is the default MongoDB port

# Choose the feature for anomaly detection (e.g., 'cpuUtilization')
feature = 'cpuUtilization'

# Specify the name of your database and collection
db_name = 'Palo_Network'
collection_name = 'ELK-Replace'

# Access the specified database and collection
db = client[db_name]
collection = db[collection_name]

# Initialize an empty list to store valid feature values
feature_values = []

# Iterate through the documents in the collection
for doc in collection.find():
    if feature in doc:
        feature_values.append(doc[feature])

# Check if there are values to calculate statistics
if not feature_values:
    print("No data available for anomaly detection.")
else:
    # Calculate mean and standard deviation of the feature
    mean = np.nanmean(feature_values)  # Use np.nanmean to handle NaN values
    std_dev = np.nanstd(feature_values)  # Use np.nanstd to handle NaN values

    # Set the Z-score threshold (e.g., ±2 standard deviations)
    z_score_threshold = 2

    # Detect anomalies
    anomalies = [doc for doc in collection.find() if feature in doc and doc[feature] > 70]

    # Print or log the detected anomalies
    for anomaly in anomalies:
        print("Anomaly detected:", anomaly)
