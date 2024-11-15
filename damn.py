from web3 import Web3
from web3.exceptions import ContractLogicError

# Base Chain Node Connection (Replace with your provider)
base_rpc_url = "https://mainnet.base.org"  # Replace with your RPC provider if different
web3 = Web3(Web3.HTTPProvider(base_rpc_url))

# Your wallet information
private_key = "YOUR_PRIVATE_KEY"  # Replace with your private key
wallet_address = Web3.toChecksumAddress("YOUR_WALLET_ADDRESS")  # Replace with your wallet address

# Target address to monitor
target_address = Web3.toChecksumAddress("0xC204af95b0307162118f7Bc36a91c9717490AB69")

# Standard ERC-20 ABI (only `name` function included for simplicity)
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    }
]

# Function to check if the transaction deploys a contract
def is_contract_deployment(tx_receipt):
    return tx_receipt['contractAddress'] is not None

# Function to get token name
def get_token_name(contract_address):
    try:
        contract = web3.eth.contract(address=contract_address, abi=ERC20_ABI)
        return contract.functions.name().call()
    except ContractLogicError:
        return "Unknown (Not a valid ERC-20 Token)"
    except Exception as e:
        return f"Error: {str(e)}"

# Function to execute a buy transaction
def auto_buy(contract_address):
    try:
        # Transaction details
        txn = {
            'from': wallet_address,
            'to': contract_address,
            'value': web3.toWei(0.005, 'ether'),  # Sending 0.005 ETH
            'gas': 300000,
            'gasPrice': web3.toWei(5, 'gwei'),
            'nonce': web3.eth.get_transaction_count(wallet_address),
        }

        # Sign the transaction
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)

        # Send the transaction
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        print(f"Auto-buy successful! Transaction hash: {tx_hash.hex()}")
    except Exception as e:
        print(f"Error during auto-buy: {e}")

# Monitoring Function
def monitor_deployments():
    print(f"Monitoring address: {target_address} on Base chain")
    latest_block = web3.eth.block_number

    while True:
        current_block = web3.eth.block_number
        if current_block > latest_block:
            for block_num in range(latest_block + 1, current_block + 1):
                block = web3.eth.get_block(block_num, full_transactions=True)
                for tx in block.transactions:
                    if tx['from'] == target_address:
                        tx_receipt = web3.eth.get_transaction_receipt(tx.hash)
                        if is_contract_deployment(tx_receipt):
                            contract_address = tx_receipt['contractAddress']
                            token_name = get_token_name(contract_address)
                            print(f"New token deployed at {contract_address} in block {block_num}")
                            print(f"Token Name: {token_name}")

                            # Execute auto-buy
                            print("Attempting auto-buy...")
                            auto_buy(contract_address)
            latest_block = current_block

if __name__ == "__main__":
    monitor_deployments()
