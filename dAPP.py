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
    return web3_connection.isConnected()

def get_nonce(ETH_address):
    return web3_connection.eth.getTransactionCount(ETH_address)

# investor donates coins to the community wallet (aka facilitator node)
def donate(investor, wallet, amount, signature):
    try:
        icw              = web3_connection.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
        transaction_body = {
            'nonce': get_nonce(investor),
            'gasPrice': icw.web3.eth.gas_price(),
            'to': wallet,
            'value': web3_connection.toWei(amount, 'ether')
        }

        function_call      = icw.functions.invest(web3_connection.toWei(amount, 'ether')).buildTransaction(transaction_body)
        signed_transaction = web3_connection.eth.account.sign_transaction(function_call, signature)
        result             = web3_connection.eth.sendRawTransaction(signed_transaction.rawTransaction)
        print(bytes(result).hex())
        return True
    except:
        return False

# community wallet (aka facilitator node) gives coins to the project participant
def disperse(wallet, project_participant, amount, signature):
    try:
        icw              = web3_connection.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
        transaction_body = {
            'nonce': get_nonce(wallet),
            'gasPrice': icw.web3.eth.gas_price(),
            'to': project_participant,
            'value': web3_connection.toWei(amount, 'ether')
        }

        function_call      = icw.functions.disperseCoin(wallet, project_participant, web3_connection.toWei(amount, 'ether')).buildTransaction(transaction_body)
        signed_transaction = web3_connection.eth.account.sign_transaction(function_call, signature)
        result             = web3_connection.eth.sendRawTransaction(signed_transaction.rawTransaction)
        print(bytes(result).hex())
        return True
    except:
        return False


if __name__ == "__main__":
    if are_we_connected():
        #investor donating coin to community wallet
        donate(os.environ['ADDRESS_INVESTOR'], os.environ['ADDRESS_WALLET'], 10, os.environ['PRIVATE_KEY_INVESTOR']) #success
        # donate(os.environ['ADDRESS_INVESTOR'], os.environ['ADDRESS_WALLET'], -1000, os.environ['PRIVATE_KEY_INVESTOR'])  #fail

        #project_participants getting their coins (Appro)
        # project_participants = {
        #     '0xEF761457FEef91242057EeBAB5FdFe533970F71C': 10,
        #     '0x599Fc7196F6138DEC843a0D5ED6299C3812056C5': 15,
        #     os.environ['ADDRESS_PROJPARTICIPANT']: 25
        # }
        # for project_participant, equity in project_participants.items():
        #     disperse(os.environ['ADDRESS_WALLET'], project_participant, equity, os.environ['PRIVATE_KEY_WALLET'])   #success

        # disperse(os.environ['ADDRESS_WALLET'], os.environ['ADDRESS_PROJPARTICIPANT'], -100, os.environ['PRIVATE_KEY_WALLET']) #fail
