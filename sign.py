import eth_account
from web3 import Web3
from eth_account.messages import encode_defunct

def sign(m):
    w3 = Web3()
    
    account = eth_account.Account.create()
    eth_address = account.address
    private_key = account.key

    message = encode_defunct(text=m)
    
    signed_message = eth_account.Account.sign_message(message, private_key=private_key)

    assert isinstance(signed_message, eth_account.datastructures.SignedMessage)

    return eth_address, signed_message
