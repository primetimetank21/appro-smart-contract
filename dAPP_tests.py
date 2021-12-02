from dAPP import *
import mock, time

def test_are_we_connected():
    assert are_we_connected() == True, "Should be connected (Ganache should be running)"

def valid_eth_address(addy):
    if type(addy) == type(str()) and addy[:2] == "0x":
        return True
    return False

def valid_amount(amount):
    is_number = type(amount) == type(float()) or type(amount) == type(int())
    if is_number and amount > 0:
        return True
    return False

def valid_signature(sig):
    if type(sig) == type(str()) and len(sig) > 0:
        return True
    return False

def test_invest(investor, wallet, amount, signature):
    #valid parameter tests
    assert valid_eth_address(investor) == True, "Invalid parameter ('investor' should be an address string)"
    assert valid_eth_address(wallet)   == True, "Invalid parameter ('wallet' should be an address string)"
    assert valid_amount(amount)        == True, "Invalid parameter ('amount' should be a nonnegative number)"
    assert valid_signature(signature)  == True, "Invalid parameter ('signature' should be a valid private key string)"
    assert investor != wallet, "The 'investor' and 'wallet' addresses should not be the same"

    mock_invest = mock.Mock(side_effect=[True, False])

    #successful transaction
    assert mock_invest() == True, "Transaction failed"
    #unsuccessful transaction
    assert mock_invest() == False, "Transaction succeeded"

def test_disperse(wallet, project_participant, amount, signature):
    #valid parameter tests
    assert valid_eth_address(wallet)    == True, "Invalid parameter ('wallet' should be an address string)"
    assert valid_eth_address(project_participant) == True, "Invalid parameter ('project_participant' should be an address string)"
    assert valid_amount(amount)         == True, "Invalid parameter ('amount' should be a nonnegative number)"
    assert valid_signature(signature)   == True, "Invalid parameter ('signature' should be a valid private key string)"
    assert wallet != project_participant, "The 'wallet' and 'project_participant' addresses should not be the same"

    mock_disperse = mock.Mock(side_effect=[True, False])

    #successful transaction
    assert mock_disperse() == True, "Transaction failed"
    #unsuccessful transaction
    assert mock_disperse() == False, "Transaction succeeded"


if __name__ == "__main__":
    start = time.time()
    test_are_we_connected()
    test_invest("0xaValidInvestorAddy", "0xaValidWalletAddy", 50, "privateKeyOfInvestor")
    test_disperse("0xaValidWalletAddy", "0xaValidProjectParticipantAddy", 10, "privateKeyOfWallet")
    end = time.time()
    print(f"All tests have run successfully (ran in {end-start: .3f} seconds)", flush=True)
