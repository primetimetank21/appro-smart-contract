pragma solidity >=0.7.0 <0.9.0;

contract ICW { //Contract representing the community wallet
    
    address communityWallet; //address of the community wallet
    mapping(address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    
    constructor (address payable _communityWallet) {
        communityWallet = _communityWallet;
    }
    

    function invest(uint256 _value) public returns (bool success) {
        if (balances[msg.sender] >= _value && _value > 0) {
            balances[msg.sender] -= _value;
            balances[communityWallet] += _value;
            emit Transfer(msg.sender, communityWallet, _value);
            return true;
        } else { return false; }
    }
    

    function getBalance() view public returns (uint256) {
        return balances[communityWallet];
    }

    
    //note: allows for the transfer of coin from _communityWallet (i.e. anyone) to _to; might be changed in the future
    function disperseCoin(address payable _communityWallet, address payable _to, uint256 _value) public returns (bool success) {
        if (balances[_communityWallet] >= _value && allowed[_communityWallet][msg.sender] >= _value && balances[_to] + _value > balances[_to]) {
            //If you have enough money AND allowed.... AND balance of CW + value sent > balance of CW
            balances[_to] += _value;
            balances[_communityWallet] -= _value;
            allowed[_communityWallet][msg.sender] -= _value;
            emit Transfer(_communityWallet, _to, _value);
            return true;
        } else { return false; }
    }

}
