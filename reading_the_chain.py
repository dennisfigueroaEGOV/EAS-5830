import random
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.providers.rpc import HTTPProvider
import os


# If you use one of the suggested infrastructure providers, the url will be of the form
# now_url  = f"https://eth.nownodes.io/{now_token}"
# alchemy_url = f"https://eth-mainnet.alchemyapi.io/v2/{alchemy_token}"
# infura_url = f"https://mainnet.infura.io/v3/{infura_token}"

def connect_to_eth():
	url = "https://eth-mainnet.g.alchemy.com/v2/UKbhl2VCaO7dWg50txaal9qiLjV2quPt"
	w3 = Web3(HTTPProvider(url))
	assert w3.is_connected(), f"Failed to connect to provider at {url}"
	return w3


def connect_with_middleware(contract_json):
	script_dir = os.path.dirname(os.path.abspath(__file__))

	# Construct the path to the JSON file
	json_location = os.path.join(script_dir, contract_json)

	with open(json_location, "r") as f:
		d = json.load(f)
		d = d['bsc']
		address = d['address']
		abi = d['abi']

	# TODO complete this method
	# The first section will be the same as "connect_to_eth()" but with a BNB url
	url = "https://data-seed-prebsc-1-s1.bnbchain.org:8545"  # FILL THIS IN
	w3 = Web3(HTTPProvider(url))
	assert w3.is_connected(), f"Failed to connect to provider at {url}"

	# The second section requires you to inject middleware into your w3 object and
	# create a contract object. Read more on the docs pages at https://web3py.readthedocs.io/en/stable/middleware.html
	# and https://web3py.readthedocs.io/en/stable/web3.contract.html

	w3.middleware_onion.inject(geth_poa_middleware, layer=0)
	contract = w3.eth.contract(address=address, abi=abi)

	return w3, contract


def is_ordered_block(w3, block_num):
	"""
	Takes a block number
	Returns a boolean that tells whether all the transactions in the block are ordered by priority fee

	Before EIP-1559, a block is ordered if and only if all transactions are sorted in decreasing order of the gasPrice field

	After EIP-1559, there are two types of transactions
		*Type 0* The priority fee is tx.gasPrice - block.baseFeePerGas
		*Type 2* The priority fee is min( tx.maxPriorityFeePerGas, tx.maxFeePerGas - block.baseFeePerGas )

	Conveniently, most type 2 transactions set the gasPrice field to be min( tx.maxPriorityFeePerGas + block.baseFeePerGas, tx.maxFeePerGas )
	"""
	block = w3.eth.get_block(block_num)
	ordered = False

	if len(block['transactions']) <= 1:
		return True

	base_fee = block.get('baseFeePerGas', 0)

	eip1559_flag = False
	if base_fee != 0:
		eip1559_flag = True

	prev_gas = None

	for tx_hash in block['transactions']:
		# Get the full transaction details
		tx = eth_w3.eth.get_transaction(tx_hash)

		if eip1559_flag:
			if 'maxFeePerGas' in tx:  
				gas_price = min(tx['maxPriorityFeePerGas'], tx['maxFeePerGas'] - gas_price)
			else:  
				gas_price = tx['gasPrice'] - gas_price
		else:  
			gas_price = tx['gasPrice']
			
		if prev_gas is not None and gas_price > prev_gas:
			return False

		prev_gas = gas_price

	return True


def get_contract_values(contract, admin_address, owner_address):
	"""
	Takes a contract object, and two addresses (as strings) to be used for calling
	the contract to check current on chain values.
	The provided "default_admin_role" is the correctly formatted solidity default
	admin value to use when checking with the contract
	To complete this method you need to make three calls to the contract to get:
	  onchain_root: Get and return the merkleRoot from the provided contract
	  has_role: Verify that the address "admin_address" has the role "default_admin_role" return True/False
	  prime: Call the contract to get and return the prime owned by "owner_address"

	check on available contract functions and transactions on the block explorer at
	https://testnet.bscscan.com/address/0xaA7CAaDA823300D18D3c43f65569a47e78220073
	"""
	default_admin_role = int.to_bytes(0, 32, byteorder="big")

	# TODO complete the following lines by performing contract calls
	onchain_root = 0  # Get and return the merkleRoot from the provided contract
	has_role = 0  # Check the contract to see if the address "admin_address" has the role "default_admin_role"
	prime = 0  # Call the contract to get the prime owned by "owner_address"

	return onchain_root, has_role, prime


"""
	This might be useful for testing (main is not run by the grader feel free to change 
	this code anyway that is helpful)
"""
if __name__ == "__main__":
	# These are addresses associated with the Merkle contract (check on contract
	# functions and transactions on the block explorer at
	# https://testnet.bscscan.com/address/0xaA7CAaDA823300D18D3c43f65569a47e78220073
	eth_w3 = connect_to_eth()
	if eth_w3.is_connected():
		print("Successfully connected to Ethereum network")
		
	else:
		print("Unable to connect")
		# Print the current block number

