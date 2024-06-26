import pandas as pd
from datetime import datetime

# Objective of this file: Merge The Graph dates with Chainlink Dates 
# There is not a data point every 5 minutes on Chainlink, so this script chooses the relevant 5 minute interval for each chainlink data point.

CHAIN = 'arbitrum'

QUERIED_DATA_FILENAME = f'queried_data_{CHAIN}.csv'
CHAINLINK_DATA_FILENAME = f'chainlink_round_data_{CHAIN}.csv'
CHAINLINK_DATA_FILENAME = 'chainlink_round_data_arbitrum-mainnet_ezETH.csv'
OUTPUT_DATA_FILENAME = f'updated_queried_data_{CHAIN}.csv'

# Load queried_date.csv and chainlink_round_data.csv into pandas DataFrames
queried_data = pd.read_csv(QUERIED_DATA_FILENAME)
chainlink_data = pd.read_csv(CHAINLINK_DATA_FILENAME)

# Convert 'Formatted Timestamp' columns to datetime objects for easier comparison
queried_data['Formatted Timestamp'] = pd.to_datetime(queried_data['Formatted Timestamp'], format='%d-%m-%Y %H:%M:%S')
chainlink_data['Formatted Timestamp'] = pd.to_datetime(chainlink_data['Formatted Timestamp'], format='%d-%m-%Y %H:%M:%S')

# Initialize empty lists to store new columns
round_timestamps = []
round_answers = []

# Iterate through each row in queried_data to find the closest timestamp match in chainlink_data
for index, row in queried_data.iterrows():
    queried_timestamp = row['Formatted Timestamp']
    
    # Find the closest timestamp in chainlink_data that is earlier or equal to queried_timestamp
    closest_row = chainlink_data[chainlink_data['Formatted Timestamp'] <= queried_timestamp].iloc[-1]
    
    # Extract data from closest_row
    closest_timestamp = closest_row['Formatted Timestamp']
    closest_answer = closest_row['Answer (ETH)']
    
    # Append to lists
    round_timestamps.append(closest_timestamp)
    round_answers.append(closest_answer)

# Add new columns to queried_data
queried_data['Round Timestamp'] = round_timestamps
queried_data['Round Answer (ETH)'] = round_answers

# Save the updated queried_data to a new CSV file
queried_data.to_csv(OUTPUT_DATA_FILENAME, index=False)

print(f"Data updated and saved to {OUTPUT_DATA_FILENAME}")