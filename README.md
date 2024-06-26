# ezeth_depeg

## Objective
Analysis of the ezETH Depeg event in April 2024, focused on the ezETH / WETH Balancer pool on Mainnet, and the ezETH / wstETH Balancer pool on Arbitrum.

## Files
- get_block_numbers.py: Get the block numbers corresponding to the times of the depeg, both on Mainnet and Arbitrum
- grt_balancer.py: Get Pool TVL Data on the relevant block numbers from The Graph, both on Mainnet and Arbitrum
- chainlink_price_data_ethereum.py: Get ezETH Price data from Chainlink on Mainnet
- chainlink_price_data_arbitrum.py: Get ezETH Price data from Chainlink on Arbitrum
- file_merge.py: Merge balancer pool data & chainlink data on the right datetime

## Technical requirements
- Using Python 3.10.9
- `pip install -r requirements.txt`