from web3 import Web3
import json
from web3.middleware import geth_poa_middleware
from eth_account.messages import encode_defunct
import random

w3 = Web3(Web3.HTTPProvider('https://api.avax-test.network/ext/bc/C/rpc'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract_address = Web3.to_checksum_address("0x85ac2e065d4526FBeE6a2253389669a12318A412")

with open('NFT.abi', 'r') as f:
    abi = json.load(f)

contract = w3.eth.contract(address=contract_address, abi=abi)

def signChallenge(challenge):
    w3 = Web3()

    sk = "e3ba163365a5bac2882ff5c80893a7479c4e97e5bd3c2a9586c3f7fe36ba6749"

    acct = w3.eth.account.from_key(sk)

    signed_message = w3.eth.account.sign_message(challenge, private_key=acct._private_key)

    return acct.address, signed_message.signature



def verifySig():
    """
        This is essentially the code that the autograder will use to test signChallenge
        We've added it here for testing
    """

    challenge_bytes = random.randbytes(32)

    challenge = encode_defunct(challenge_bytes)
    address, sig = signChallenge(challenge)

    w3 = Web3()

    return w3.eth.account.recover_message(challenge, signature=sig) == address

def mint_nft(private_key):
    account = w3.eth.account.from_key(private_key)
    nonce = w3.eth.get_transaction_count(account.address)

    claim_nonce = 13379

    tx = contract.functions.claim(claim_nonce).build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price,
    })

    signed_transaction = account.sign_transaction(tx)
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

    if receipt.status == 1:
        print("NFT minted!!")
        return True
    else:
        print("Didn't mint NFT :(")
        return False

if __name__ == '__main__':
    """
        Test your function
    """

    private_key = "e3ba163365a5bac2882ff5c80893a7479c4e97e5bd3c2a9586c3f7fe36ba6749"

    if mint_nft(private_key):
        print("Minted the nft.")
    else:
        print("Did not mint nft.")


    if verifySig():
        print(f"You passed the challenge!")
    else:
        print(f"You failed the challenge!")

