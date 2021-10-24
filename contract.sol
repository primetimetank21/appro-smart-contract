pragma solidity >=0.7.0 <0.9.0;

contract ICW { //Contract between the investor and the community wallet
    
    //address owner; //This is the owner of the contract (investor)
    address communityWallet; //Address of the community wallet
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
    
    // function getBalance() view public returns (uint256) {
    //     return balances[communityWallet];
    // }

    
    //     function transferFrom(address payable _from, address payable _communityWallet, uint256 _value) public returns (bool success) {
    // //same as above. Replace this line with the following if you want to protect against wrapping uints.
    //     if (balances[_from] >= _value && allowed[_from][msg.sender] >= _value && balances[_communityWallet] + _value > balances[_communityWallet]) {
    //         //If you have enough money AND allowed.... AND balance of CW + value sent > balance of CW
    //     //if (balances[_from] >= _value && allowed[_from][msg.sender] >= _value && _value > 0) {
    //         balances[_communityWallet] += _value;
    //         balances[_from] -= _value;
    //         allowed[_from][msg.sender] -= _value;
    //         emit Transfer(_from, _communityWallet, _value);
    //         return true;
    //     } else { return false; }
    // }

}

