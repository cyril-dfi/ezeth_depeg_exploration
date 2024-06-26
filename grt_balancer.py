import requests
import json
import csv
import time
from datetime import datetime

CHAIN = 'arbitrum'

# Define the GraphQL endpoint for Balancer on The Graph
API_KEY = '<INSERT_KEY_HERE>'

# Define the CSV file names
INPUT_CSV_FILENAME = f'block_numbers_{CHAIN}.csv'
OUTPUT_CSV_FILENAME = f'queried_data_{CHAIN}.csv'

GRAPH_IDS = {}
GRAPH_IDS['ethereum'] = 'C4ayEZP2yTXRAB8vSaTrgN4m9anTe9Mdm2ViyiAuV9TV'
GRAPH_IDS['arbitrum'] = '98cQDy6tufTJtshDCuhh9z2kWXsQWBHVh2bqnLHsGAeS'

POOL_IDS = {}
POOL_IDS['ethereum'] = '0x596192bb6e41802428ac943d2f1476c1af25cc0e000000000000000000000659'
POOL_IDS['arbitrum'] = '0xb61371ab661b1acec81c699854d2f911070c059e000000000000000000000516'


url = f"https://gateway-arbitrum.network.thegraph.com/api/{API_KEY}/subgraphs/id/{GRAPH_IDS[CHAIN]}"

# Function to read block numbers and timestamps from CSV
def read_block_numbers_and_timestamps_from_csv(filename):
    blocks = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            block_number = row[1]  # Assuming 'Block Number' is in the second column
            timestamp = row[0]  # Assuming 'Timestamp' is in the third column
            blocks.append({'block_number': block_number, 'timestamp': timestamp})
    return blocks

# Function to query data for a block number
def query_graphql_for_block_number(block_number):
    query = """
    {
      pool(id: "%s", block: { number: %s }) {
        id
        address
        tokens {
          address
          balance
          symbol
        }
        totalSwapVolume
        totalSwapFee
      }
    }
    """ % (POOL_IDS[CHAIN], block_number)

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps({"query": query}))

    if response.status_code == 200:
        return response.json()['data']['pool']
    else:
        print(f"Query failed for block number {block_number}. Status code: {response.status_code}")
        return None

# Function to save queried data to CSV
def save_queried_data_to_csv(data, blocks, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write header row
        header = ['Block Number', 'Timestamp', 'Formatted Timestamp', 'Pool ID', 'Total Swap Volume', 'Total Swap Fee']
        tokens_columns = set()  # To store unique token symbols as column headers

        # Collect all unique token symbols
        for pool_data in data:
            if pool_data:
                for token_data in pool_data['tokens']:
                    tokens_columns.add(token_data['symbol'])

        # Add token symbols as headers
        header.extend(sorted(tokens_columns))

        writer.writerow(header)

        # Write data rows
        for i, pool_data in enumerate(data):
            if pool_data:
                row = [
                    blocks[i]['block_number'],  # Block Number
                    blocks[i]['timestamp'],  # Timestamp
                    datetime.utcfromtimestamp(int(blocks[i]['timestamp'])).strftime('%d-%m-%Y %H:%M:%S'),  # Formatted Timestamp
                    pool_data['id'],  # Pool ID
                    pool_data['totalSwapVolume'],  # Total Swap Volume
                    pool_data['totalSwapFee']  # Total Swap Fee
                ]

                # Prepare token balances in the corresponding columns
                token_balances = {token['symbol']: token['balance'] for token in pool_data['tokens']}
                for symbol in sorted(tokens_columns):
                    row.append(token_balances.get(symbol, ''))

                writer.writerow(row)

# Main function to execute the workflow
def main():
    # Read block numbers and timestamps from input CSV
    blocks = read_block_numbers_and_timestamps_from_csv(INPUT_CSV_FILENAME)

    # List to store queried data
    queried_data = []

    # Loop through each block number and query data
    for block_info in blocks:
        block_number = block_info['block_number']
        data = query_graphql_for_block_number(block_number)
        if data:
            queried_data.append(data)
        time.sleep(0.2)  # To respect API rate limits

    # Save queried data to output CSV
    save_queried_data_to_csv(queried_data, blocks, OUTPUT_CSV_FILENAME)

    print(f"Queried data saved to {OUTPUT_CSV_FILENAME}")

# Run the main function
if __name__ == "__main__":
    main()
