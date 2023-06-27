import os
import time
from dotenv import load_dotenv
from web3 import Web3
from web3.contract import Contract

load_dotenv()

# Constants
wethAddress = '0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6'  # goerli weth
# wethAddress = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'  # mainnet weth
routerAddress = '0xE592427A0AEce92De3Edee1F18E0157C05861564'  # Uniswap Router
quoterAddress = '0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6'  # Uniswap Quoter
tokenAddress = '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984'  # goerli uni
fee = 3000  # Uniswap pool fee bps 500, 3000, 10000
buyAmount = Web3.toWei(0.001, 'ether')
targetPrice = 35  # target exchange rate
targetAmountOut = buyAmount * targetPrice
sellAmount = buyAmount / targetPrice
tradeFrequency = 3600 * 1000  # ms (once per hour)

# Ethereum provider
provider_url = f"https://eth-goerli.alchemyapi.io/v2/{os.getenv('ALCHEMY_API_KEY')}"
provider = Web3.HTTPProvider(provider_url)
web3 = Web3(provider)

# Wallet
private_key = os.getenv('PRIVATE_KEY')
account = web3.eth.account.privateKeyToAccount(private_key)

# Token Contract
token_contract = Contract.from_abi(
    "Token", address=web3.toChecksumAddress(tokenAddress),
    abi=[
        'function approve(address spender, uint256 amount) external returns (bool)',
        'function allowance(address owner, address spender) public view returns (uint256)',
    ]
)

# Router Contract
router_contract = Contract.from_abi(
    "Router", address=web3.toChecksumAddress(routerAddress),
    abi=['function exactInputSingle((address tokenIn, address tokenOut, uint24 fee, address recipient, uint256 deadline, uint256 amountIn, uint256 amountOutMinimum, uint160 sqrtPriceLimitX96)) external payable returns (uint256 amountOut)']
)

# Quoter Contract
quoter_contract = Contract.from_abi(
    "Quoter", address=web3.toChecksumAddress(quoterAddress),
    abi=['function quoteExactInputSingle(address tokenIn, address tokenOut, uint24 fee, uint256 amountIn, uint160 sqrtPriceLimitX96) public view returns (uint256 amountOut)']
)

# Buy Tokens
def buyTokens():
    print('Buying Tokens')
    deadline = int(time.time()) + 600
    tx = router_contract.functions.exactInputSingle(
        [wethAddress, tokenAddress, fee, account.address, deadline, buyAmount, 0, 0]
    ).transact({'value': buyAmount})
    web3.eth.waitForTransactionReceipt(tx)
    print(tx.hex())

# Sell Tokens
def sellTokens():
    print('Selling Tokens')
    allowance = token_contract.functions.allowance(account.address, routerAddress).call()
    print(f'Current allowance: {allowance}')
    if allowance < sellAmount:
        print('Approving Spend (bulk approve in production)')
        atx = token_contract.functions.approve(
            routerAddress, sellAmount
        ).transact({'from': account.address})
        web3.eth.waitForTransactionReceipt(atx)
    deadline = int(time.time()) + 600
    tx = router_contract.functions.exactInputSingle(
        [tokenAddress, wethAddress, fee, account.address, deadline, sellAmount, 0, 0]
    ).transact({'from': account.address})
    web3.eth.waitForTransactionReceipt(tx)
    print(tx.hex())

# Check Price
def checkPrice():
    amountOut = quoter_contract.functions.quoteExactInputSingle(
        wethAddress, tokenAddress, fee, buyAmount, 0
    ).call()
    print(f'Current Exchange Rate: {amountOut}')
    print(f'Target Exchange Rate: {targetAmountOut}')
    if amountOut < targetAmountOut:
        buyTokens()
    if amountOut > targetAmountOut:
        sellTokens()

checkPrice()
while True:
    time.sleep(tradeFrequency / 1000)
    checkPrice()

