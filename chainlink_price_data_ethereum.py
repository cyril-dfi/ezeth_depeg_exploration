from web3 import Web3
from datetime import datetime, timezone
import time
import csv

def format_answer(answer):
    # Format timestamp to human-readable format
    timestamp = answer[2]

    # Convert the timestamp to a datetime object in UTC
    utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)

    # Format the datetime object
    formatted_timestamp = utc_time.strftime('%d-%m-%Y %H:%M:%S')

    # Return formatted timestamp and answer (converted to ETH)
    return formatted_timestamp, answer[1] / (10 ** 18)


infura_key = "<INSERT_KEY_HERE>"
network = 'mainnet'

rpc_url = f'https://{network}.infura.io/v3/{infura_key}'
web3 = Web3(Web3.HTTPProvider(rpc_url))

# AggregatorV3Interface ABI
abi = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
# Price Feed address
addr = '0x636A000262F6aA9e1F094ABF0aD8f645C44f641C'

# Set up contract instance
contract = web3.eth.contract(address=addr, abi=abi)
# Make call to latestRoundData()
# latestData = contract.functions.latestRoundData().call()
# print(format_answer(latestData))

# Use this contract to get list of valid roundId: https://etherscan.io/address/0xd32fb8bf0decc9a80968e480694fa60e3e91895c#readContract
round_ids = [18446744073709551950,18446744073709551951,18446744073709551952,18446744073709551953,18446744073709551954,18446744073709551955,18446744073709551956,18446744073709551957,18446744073709551958,18446744073709551959,18446744073709551960,18446744073709551961,18446744073709551962,18446744073709551963,18446744073709551964,18446744073709551965,18446744073709551966,18446744073709551967,18446744073709551968,18446744073709551969,18446744073709551970,18446744073709551971,18446744073709551972,18446744073709551973,18446744073709551974,18446744073709551975,18446744073709551976,18446744073709551977,18446744073709551978,18446744073709551979,18446744073709551980,18446744073709551981,18446744073709551982,18446744073709551983,18446744073709551984,18446744073709551985,18446744073709551986,18446744073709551987,18446744073709551988,18446744073709551989,18446744073709551990,18446744073709551991,18446744073709551992,18446744073709551993,18446744073709551994,18446744073709551995,18446744073709551996,18446744073709551997,18446744073709551998,18446744073709551999,18446744073709552000,18446744073709552001,18446744073709552002,18446744073709552003,18446744073709552004,18446744073709552005,18446744073709552006,18446744073709552007,18446744073709552008,18446744073709552009,18446744073709552010,18446744073709552011,18446744073709552012,18446744073709552013,18446744073709552014,18446744073709552015,18446744073709552016,18446744073709552017,18446744073709552018,18446744073709552019,18446744073709552020,18446744073709552021,18446744073709552022,18446744073709552023,18446744073709552024,18446744073709552025,18446744073709552026,18446744073709552027,18446744073709552028,18446744073709552029,18446744073709552030,18446744073709552031,18446744073709552032,18446744073709552033,18446744073709552034,18446744073709552035,18446744073709552036,18446744073709552037,18446744073709552038,18446744073709552039,18446744073709552040,18446744073709552041,18446744073709552042,18446744073709552043,18446744073709552044,18446744073709552045,18446744073709552046,18446744073709552047,18446744073709552048,18446744073709552049,18446744073709552050,18446744073709552051,18446744073709552052,18446744073709552053,18446744073709552054,18446744073709552055,18446744073709552056,18446744073709552057,18446744073709552058,18446744073709552059,18446744073709552060,18446744073709552061,18446744073709552062,18446744073709552063,18446744073709552064]


# List to hold formatted results
formatted_results = []

# Perform queries and store results
for round_id in round_ids:
    try:
        historical_data = contract.functions.getRoundData(round_id).call()
        # [18446744073709552329, 1001968774687151700, 1718922251, 1718922251, 18446744073709552329]
        formatted_result = format_answer(historical_data)
        formatted_results.append(formatted_result)
        time.sleep(0.1)  # Rate limit to avoid overwhelming the API
    except Exception as e:
        print(f"Error fetching data for round ID {round_id}: {str(e)}")

# Write results to a CSV file
output_csv_filename = 'chainlink_round_data.csv'
header = ['Formatted Timestamp', 'Answer (ETH)']

with open(output_csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(formatted_results)

print(f"Data saved to {output_csv_filename}")
