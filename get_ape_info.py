from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time
import os
from urllib.parse import urlparse

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.to_checksum_address(bayc_address)

# You will need the ABI to connect to the contract
# The file 'abi.json' has the ABI for the bored ape contract
# In general, you can get contract ABIs from etherscan
# https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('/home/codio/workspace/abi.json', 'r') as f:
	abi = json.load(f)

############################
# Connect to an Ethereum node

api_url = "https://eth-mainnet.g.alchemy.com/v2/UKbhl2VCaO7dWg50txaal9qiLjV2quPt"
provider = HTTPProvider(api_url)
web3 = Web3(provider)


def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), f"get_from_ipfs accepts a cid in the form of a string"
    url = f"https://gateway.pinata.cloud/ipfs/{cid}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        if content_type.lower() == "json":
            data = response.json()
        else:
            raise ValueError("It is required to be of type JSON.")
        assert isinstance(data, dict), f"get_from_ipfs should return a dict"
    except requests.exceptions.RequestException as e:
        print(f"Issue happened while retrieving from IPFS: {e}")
        return None
    return data


def get_ape_info(apeID):
    assert isinstance(apeID, int), f"{apeID} is not an int"
    assert 1 <= apeID, f"{apeID} must be at least 1"

    data = {'owner': "", 'image': "", 'eyes': ""}

    contract = web3.eth.contract(address=contract_address, abi=abi)

    try:
        data['owner'] = contract.functions.ownerOf(apeID).call()
        token_uri = contract.functions.tokenURI(apeID).call()
        ipfs_path = token_uri.split('ipfs://')[1]
        metadata = get_from_ipfs(ipfs_path)

        if metadata:
            data['image'] = metadata.get('image', '')

            for attribute in metadata.get('attributes', []):
                if attribute.get('trait_type') == 'Eyes':
                    data['eyes'] = attribute.get('value', '')
                    break
        else:
            print(f'No metadata able to be retrieved for Ape {apeID}')

    except Exception as e:
        print(f"An error occurred: {e}")

    # print(data)
    # print(f'The cid is: {ipfs_path}')
    # print(f'The metadata is: {metadata}')
    # image = metadata.get('image', '')
    # print(f'The metadata image is: {image}')

    assert isinstance(data, dict), f'get_ape_info{apeID} should return a dict'
    assert all([a in data.keys() for a in
                ['owner', 'image', 'eyes']]), f"return value should include the keys 'owner','image' and 'eyes'"
    return data


# get_ape_info(7495)
