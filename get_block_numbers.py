import requests
import time
import csv
from datetime import datetime, timedelta

CHAIN = 'arbitrum'

# Etherscan API key
API_KEYS = {}
API_KEYS['ethereum'] = '<INSERT_KEY_HERE>'
API_KEYS['arbitrum'] = '<INSERT_KEY_HERE>'

URLS = {}
URLS['ethereum'] = 'https://api.etherscan.io/api'
URLS['arbitrum'] = 'https://api.arbiscan.io/api'

# Function to get block number by timestamp using Etherscan/Arbiscan API
def get_block_number_by_timestamp(timestamp):
    url = URLS[CHAIN]
    params = {
        'module': 'block',
        'action': 'getblocknobytime',
        'timestamp': timestamp,
        'closest': 'before',
        'apikey': API_KEYS[CHAIN]
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['result']

# Generate timestamps every 5 minutes from April 23rd to April 25th
start_time = datetime(2024, 4, 23)
end_time = datetime(2024, 4, 25)
interval = timedelta(minutes=5)
timestamps = []

current_time = start_time
while current_time <= end_time:
    timestamps.append(int(current_time.timestamp()))
    current_time += interval

# Fetch block numbers for each timestamp
block_numbers = []
for timestamp in timestamps:
    block_number = get_block_number_by_timestamp(timestamp)
    block_numbers.append((timestamp, block_number))
    time.sleep(0.2)  # To respect API rate limits

# Print the results
for timestamp, block_number in block_numbers:
    print(f"Timestamp: {datetime.fromtimestamp(timestamp)} - Block Number: {block_number}")


# Save results to a CSV file
csv_filename = f'block_numbers_{CHAIN}.csv'
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Block Number'])
    for timestamp, block_number in block_numbers:
        writer.writerow([timestamp, block_number])