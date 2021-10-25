import os
import json
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()
node_provider     = os.environ['NODE_PROVIDER_LOCAL']
web3_connection   = Web3(Web3.HTTPProvider(node_provider))
contract_abi      = json.loads(os.environ['CONTRACT_ABI'])
contract_bytecode = os.environ['CONTRACT_BYTECODE']
# contract_address  = os.environ['CONTRACT_ADDRESS']
# contract_address  = '0x375Fde61EE0905454f5a54e2a1d72A9be437298a'

def are_we_connected():
    print(web3_connection.isConnected())

def get_nonce(ETH_address):
    return web3_connection.eth.getTransactionCount(ETH_address)

def invest(investor, wallet, amount, signature):
    icw              = web3_connection.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    transaction_body = {
        'nonce': get_nonce(investor),
        'gasPrice': icw.web3.eth.gas_price(),
        'to': wallet,
        'value': web3_connection.toWei(amount, 'ether')
    }

    # function_call      = icw.functions.transferFrom2(investor, wallet, amount).buildTransaction(transaction_body)
    function_call      = icw.functions.invest(web3_connection.toWei(amount, 'ether')).buildTransaction(transaction_body)
    signed_transaction = web3_connection.eth.account.sign_transaction(function_call, signature)
    result             = web3_connection.eth.sendRawTransaction(signed_transaction.rawTransaction)
    print(bytes(result).hex())
    return result


if __name__ == "__main__":
    are_we_connected()
    invest(os.environ['ADDRESS_INVESTOR'], os.environ['ADDRESS_WALLET'], 10, os.environ['PRIVATE_KEY_INVESTOR']) #success
    # invest(os.environ['ADDRESS_INVESTOR'], os.environ['ADDRESS_WALLET'], 100, os.environ['PRIVATE_KEY_INVESTOR'])  #fail