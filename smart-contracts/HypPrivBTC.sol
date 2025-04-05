// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.0;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@hyperlane-xyz/core/contracts/interfaces/IMailbox.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC20Burnable} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract PrivCoin is ERC20, ERC20Burnable {

    event InitializeAddress(address indexed user, uint256 share1, uint256 share2, uint256 share3);
    event Deposit(address indexed user, uint256 share1, uint256 share2, uint256 share3);
    event Withdraw(address indexed user, uint256 share1, uint256 share2, uint256 share3);
    event Transfer(address indexed user, address indexed receiver, uint256 share1, uint256 share2, uint256 share3);

    address public mailbox;
    uint256 public party1_public_key;
    uint256 public party2_public_key;
    uint256 public party3_public_key;
    uint256 public rsa_n;
    uint256 public mpc_prime;

    mapping (address => bool) public initializedAddress;
    address owner;

    constructor(address _mailbox, uint256 _party1_public_key, uint256 _party2_public_key, uint256 _party3_public_key, uint256 _rsa_n, uint256 _mpc_prime) ERC20("Bridged cBTC", "bcBTC") {
        mailbox = _mailbox;
        party1_public_key = _party1_public_key;
        party2_public_key = _party2_public_key;
        party3_public_key = _party3_public_key;
        rsa_n = _rsa_n;
        mpc_prime = _mpc_prime;
        owner = msg.sender;
    }

    function changeKeys(uint256 _k1, uint256 _k2, uint256 _k3) external{
        require(msg.sender==owner, "Only owner");
        party1_public_key = _k1;
        party2_public_key = _k2;
        party3_public_key = _k3;
    }

    function intializeAddress(uint256 _share1, uint256 _share2, uint256 _share3) external {
        require(!initializedAddress[msg.sender], "Already initialized");
        initializedAddress[msg.sender] = true;
        emit InitializeAddress(msg.sender, _share1, _share2, _share3);
    }

    function deposit(uint256 _value, uint256 _share1, uint256 _share2, uint256 _share3) external{
        _burn(msg.sender, _value);
        emit Deposit(msg.sender, _share1, _share2, _share3);
    }

    function transfer(address receiver, uint256 _user_share1, uint256 _user_share2, uint256 _user_share3, uint256 _share1, uint256 _share1sign, uint256 _share2, uint256 _share2sign, uint256 _share3, uint256 _share3sign) external{
        require((_share1sign**party1_public_key)%rsa_n==_share1, "Invalid signature !!!");
        require((_share2sign**party2_public_key)%rsa_n==_share2, "Invalid signature !!!");
        require((_share3sign**party3_public_key)%rsa_n==_share3, "Invalid signature !!!");
        uint256 sum = (_share1+_share2+_share3)%mpc_prime;
        require(sum < mpc_prime/2, "Insufficient Balance");
        emit Transfer(msg.sender, receiver, _user_share1, _user_share2, _user_share3);
    }

    function withdraw(uint256 _claim, uint256 _share1, uint256 _share1_sign, uint256 _share2, uint256 _share2_sign, uint256 _share3, uint256 _share3_sign) external{
        require((_share1_sign**party1_public_key)%rsa_n==_share1, "Invalid signature !!!");
        require((_share2_sign**party2_public_key)%rsa_n==_share2, "Invalid signature !!!");
        require((_share3_sign**party3_public_key)%rsa_n==_share3, "Invalid signature !!!");
        uint256 sum = (_share1+_share2+_share3)%mpc_prime;
        require(sum==0, "Invalid balance");
        _mint(msg.sender, _claim);
        emit Withdraw(msg.sender, _share1, _share2, _share3);
    }

    function bridgeBTC(uint32 _domainId, address _contractAddress, address _receiver, uint256 _share1, uint256 _share1_sign, uint256 _share2, uint256 _share2_sign, uint256 _share3, uint256 _share3_sign) payable external{
        require((_share1_sign**party1_public_key)%rsa_n==_share1, "Invalid signature !!!");
        require((_share2_sign**party2_public_key)%rsa_n==_share2, "Invalid signature !!!");
        require((_share3_sign**party3_public_key)%rsa_n==_share3, "Invalid signature !!!");
        uint256 sum = (_share1+_share2+_share3)%mpc_prime;
        require(sum==0, "Invalid balance");
        IMailbox _mailbox = IMailbox(mailbox);
        _mailbox.dispatch{value: msg.value}(_domainId, addressToBytes32(_contractAddress), abi.encode(_receiver, _share1, _share2, _share3));
        emit Withdraw(msg.sender, _share1, _share2, _share3);
    }

    function handle(uint32 _origin, bytes32 _sender, bytes calldata _message) external payable{
        require(msg.sender == mailbox, "Only mailbox can call this function");
        (address receiver, uint256 share1, uint256 share2, uint256 share3) = abi.decode(_message, (address, uint256, uint256, uint256));
        emit Deposit(receiver, share1, share2, share3);
    }

    function addressToBytes32(address _addr) internal pure returns (bytes32) {
        return bytes32(uint256(uint160(_addr)));
    }

    function bytes32ToAddress(bytes32 _buf) internal pure returns (address) {
        return address(uint160(uint256(_buf)));
    }

}