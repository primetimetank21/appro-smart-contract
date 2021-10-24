import os
import json
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()
node_provider     = os.environ['NODE_PROVIDER_LOCAL']
web3_connection   = Web3(Web3.HTTPProvider(node_provider))
contract_abi      = json.loads(os.environ['CONTRACT_ABI'])
contract_bytecode = os.environ['CONTRACT_BYTECODE']

def are_we_connected():
    print(web3_connection.isConnected())

def get_nonce(ETH_address):
    return web3_connection.eth.getTransactionCount(ETH_address)

def deploy_contract(cost, owner, signature):
    icw              = web3_connection.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    transaction_body = {
        'nonce': get_nonce(owner),
        'gasPrice': icw.web3.eth.gas_price(),
    }

    deployment         = icw.constructor(owner).buildTransaction(transaction_body)
    signed_transaction = web3_connection.eth.account.sign_transaction(deployment, signature)
    result             = web3_connection.eth.sendRawTransaction(signed_transaction.rawTransaction)
    return result

if __name__ == "__main__":
    are_we_connected()
    deploy_contract(1, os.environ['ADDRESS_WALLET'], os.environ['PRIVATE_KEY_WALLET'])