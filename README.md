# pythontradingbot
I transposed the trading bot designed by James Bachini into Python. The original work cna be found here -  

**Market Maker Bot (Python Adaptation)**

This repository contains a Python adaptation of the market maker bot originally written in JavaScript using the ethers.js library. The original code can be found here - https://github.com/jamesbachini/Market-Maker-Bot.

**Dependencies**

The Python adaptation of the market maker bot utilizes the following dependencies:
1. web3: A Python library for interacting with the Ethereum blockchain.
2. python-dotenv: A library for loading environment variables from a .env file.

**Usage**
1. Clone the repository: ```git clone https://github.com/jamesbachini/Market-Maker-Bot.git```
2. Install the required dependencies: ```pip install web3 python-dotenv```
3. Create a .env file in the root directory and provide the following environment variables:
```PROVIDER_URL=<your_ethereum_provider_url>```
```PRIVATE_KEY=<your_private_key>```
4. Modify the script (index.py) to set the desired configuration parameters, such as token addresses, fees, trade amounts, target prices, etc.
5. Run the bot: ```python index.py```

**Script Explanation**

The index.py script performs the following steps:
1. Imports the required dependencies (web3 and python-dotenv) and loads environment variables from the .env file.
2. Sets up the Ethereum provider using the specified provider URL.
3. Uses the web3 library to interact with Ethereum accounts, contracts, etc.
4. Defines functions to buy tokens, sell tokens, and check the current price.
5. Initiates the trading logic by calling the checkPrice function once.
6. Sets up a periodic interval using time.sleep to repeatedly call the checkPrice function at the specified trade frequency.

For more detailed information and the original code, please refer to the Market-Maker-Bot repository - https://github.com/jamesbachini/Market-Maker-Bot.
