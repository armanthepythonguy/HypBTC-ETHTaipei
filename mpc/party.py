import json
from prime import rsa_decrypt, find_dec_key
from web3 import Web3
import os
import time

id = os.getenv("ID")
P = 2**127-1
p,q = 49157,170141183460469231731687303715884105727
enc_list = [5,11,13]
public_key = (enc_list[int(id)-1], p*q)
print(f"Node-id: {id}")
print(f"Public Key: {public_key}")
private_key = (find_dec_key(public_key[0], (p-1)*(q-1)), p*q)

balances = {}

try:
    with open(f'{id}_balance.json') as f:
        balances = json.load(f)
except FileNotFoundError:
    print("Starting new node, no old data found !!!")

abi = '''
[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_mailbox",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_party1_public_key",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_party2_public_key",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_party3_public_key",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_rsa_n",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_mpc_prime",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "user",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "share1",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "share2",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "share3",
				"type": "uint256"
			}
		],
		"name": "Deposit",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "user",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "share1",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "share2",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "share3",
				"type": "uint256"
			}
		],
		"name": "InitializeAddress",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "user",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "receiver",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "share1",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "share2",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "share3",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "user",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "share1",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "share2",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "share3",
				"type": "uint256"
			}
		],
		"name": "Withdraw",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint32",
				"name": "_domainId",
				"type": "uint32"
			},
			{
				"internalType": "address",
				"name": "_contractAddress",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_receiver",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_share1",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_share2",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_share3",
				"type": "uint256"
			}
		],
		"name": "bridgeBTC",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_k1",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_k2",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_k3",
				"type": "uint256"
			}
		],
		"name": "changeKeys",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_share1",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_share2",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_share3",
				"type": "uint256"
			}
		],
		"name": "deposit",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint32",
				"name": "_origin",
				"type": "uint32"
			},
			{
				"internalType": "bytes32",
				"name": "_sender",
				"type": "bytes32"
			},
			{
				"internalType": "bytes",
				"name": "_message",
				"type": "bytes"
			}
		],
		"name": "handle",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "initializedAddress",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_share1",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_share2",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_share3",
				"type": "uint256"
			}
		],
		"name": "intializeAddress",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "mailbox",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "mpc_prime",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "party1_public_key",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "party2_public_key",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "party3_public_key",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "recieverContract",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "rsa_n",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "receiver",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_user_share1",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_user_share2",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_user_share3",
				"type": "uint256"
			}
		],
		"name": "transfer",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_claim",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_share1",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_share1_sign",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_share2",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_share2_sign",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_share3",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_share3_sign",
				"type": "uint256"
			}
		],
		"name": "withdraw",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]
'''

def write_balance():
    with open(f'{id}_balance.json', 'w') as f:
        f.write(json.dumps(balances))


def store_share(user_id, share):
    decrypted_share = rsa_decrypt(share, private_key)
    balances[user_id] = decrypted_share
    write_balance()
    print(balances)

def update_share_deposit(user_id, delta):
    decrypted_delta = rsa_decrypt(delta, private_key)
    balances[user_id] = (balances[user_id] + decrypted_delta) % P
    write_balance()
    print(balances)

def update_share_withdraw(user_id, delta):
    decrypted_delta = rsa_decrypt(delta, private_key)
    balances[user_id] = (balances[user_id] - decrypted_delta) % P
    write_balance()
    print(balances)

def update_share(user_id, delta, receiver_id):
    decrypted_delta = rsa_decrypt(delta, private_key)
    balances[user_id] = (balances[user_id] - decrypted_delta) % P
    balances[receiver_id] = (balances[receiver_id] + decrypted_delta) % P
    write_balance()
    print(balances)

def to_0x(hash):
    if not hash.startswith("0x"):
        return("0x" + hash)
    return hash

# Sepolia
w3 = Web3(Web3.HTTPProvider("https://arb-sepolia.g.alchemy.com/v2/jqB7OeLKcX8m2TMcinEyRBG6hXUq-kIC"))
address = "0x38f7AE184Dd3683F68D870aeFcd1B02c02b679b1"#input("Enter the sepolia contract address: ")
contract = w3.eth.contract(address=address, abi=abi)
intialize_filter = contract.events.InitializeAddress
intialize_filter_hash = Web3.keccak(text="InitializeAddress(address,uint256,uint256,uint256)").hex()
deposit_filter = contract.events.Deposit
deposit_filter_hash = Web3.keccak(text="Deposit(address,uint256,uint256,uint256)").hex()
transfer_filter = contract.events.Transfer
transfer_filter_hash = Web3.keccak(text="Transfer(address,address,uint256,uint256,uint256)").hex()
withdraw_filter = contract.events.Withdraw
withdraw_filter_hash = Web3.keccak(text="Withdraw(address,uint256,uint256,uint256)").hex()

#RootStock
rs_w3 = Web3(Web3.HTTPProvider("https://rpc.testnet.citrea.xyz"))
rs_address = "0xEa06d01bc05C26078906Ab01846a868e8BC6b6F2" #input("Enter the rootstock contract address: ")
rs_contract = rs_w3.eth.contract(address=rs_address, abi=abi)
rs_intialize_filter = rs_contract.events.InitializeAddress
rs_intialize_filter_hash = rs_w3.keccak(text="InitializeAddress(address,uint256,uint256,uint256)").hex()
rs_deposit_filter = rs_contract.events.Deposit
rs_deposit_filter_hash = rs_w3.keccak(text="Deposit(address,uint256,uint256,uint256)").hex()
rs_transfer_filter = rs_contract.events.Transfer
rs_transfer_filter_hash = rs_w3.keccak(text="Transfer(address,address,uint256,uint256,uint256)").hex()
rs_withdraw_filter = rs_contract.events.Withdraw
rs_withdraw_filter_hash = w3.keccak(text="Withdraw(address,uint256,uint256,uint256)").hex()

last_eth_block = w3.eth.block_number
last_btc_block = rs_w3.eth.block_number

while True:
    current_eth_block = w3.eth.block_number
    current_btc_block = rs_w3.eth.block_number

    if current_eth_block > last_eth_block:
        try:

            #ETH Initialize
            logs = w3.eth.get_logs({
                "fromBlock": last_eth_block + 1,
                "toBlock": current_eth_block,
                "address": contract.address,
                "topics": [to_0x(intialize_filter_hash)]
            })

            for log in logs:
                event = intialize_filter().process_log(log)
                user_id = event['args'][f'user']
                share = event['args'][f'share{id}']
                store_share(f'{w3.eth.chain_id}_{user_id}', share)
                print(f"[Block {log['blockNumber']}] Event: {event['args']}")

            #ETH Deposit
            logs = w3.eth.get_logs({
                "fromBlock": last_eth_block + 1,
                "toBlock": current_eth_block,
                "address": contract.address,
                "topics": [to_0x(deposit_filter_hash)]
            })

            for log in logs:
                event = deposit_filter().process_log(log)
                user_id = event['args'][f'user']
                share = event['args'][f'share{id}']
                update_share_deposit(f'{w3.eth.chain_id}_{user_id}', share)
                print(f"[Block {log['blockNumber']}] Event: {event['args']}")

            #ETH Transfer
            logs = w3.eth.get_logs({
                "fromBlock": last_eth_block + 1,
                "toBlock": current_eth_block,
                "address": contract.address,
                "topics": [to_0x(transfer_filter_hash)]
            })
            for log in logs:
                event = transfer_filter().process_log(log)
                user_id = event['args'][f'user']
                share = event['args'][f'share{id}']
                receiver_id = event['args']['receiver']
                update_share(f'{w3.eth.chain_id}_{user_id}', share, f'{w3.eth.chain_id}_{receiver_id}')
                print(f"[Block {log['blockNumber']}] Event: {event['args']}")

            #ETH Withdraw
            logs = w3.eth.get_logs({
                "fromBlock": last_eth_block + 1,
                "toBlock": current_eth_block,
                "address": contract.address,
                "topics": [to_0x(withdraw_filter_hash)]
            })
            for log in logs:
                event = withdraw_filter().process_log(log)
                user_id = event['args'][f'user']
                share = event['args'][f'share{id}']
                update_share_withdraw(f'{w3.eth.chain_id}_{user_id}', share)
                print(f"[Block {log['blockNumber']}] Event: {event['args']}")

            last_eth_block = current_eth_block

            #RootStock Initialize
            logs = rs_w3.eth.get_logs({
                "fromBlock": last_btc_block + 1,
                "toBlock": current_btc_block,
                "address": rs_contract.address,
                "topics": [rs_intialize_filter_hash]
            })
            for log in logs:
                event = rs_intialize_filter().process_log(log)
                user_id = event['args'][f'user']
                share = event['args'][f'share{id}']
                store_share(f'{rs_w3.eth.chain_id}_{user_id}', share)
                print(f"[Block {log['blockNumber']}] Event: {event['args']}")

            #RootStock Deposit
            logs = rs_w3.eth.get_logs({
                "fromBlock": last_btc_block + 1,
                "toBlock": current_btc_block,
                "address": rs_contract.address,
                "topics": [rs_deposit_filter_hash]
            })
            for log in logs:
                event = rs_deposit_filter().process_log(log)
                user_id = event['args'][f'user']
                share = event['args'][f'share{id}']
                update_share_deposit(f'{rs_w3.eth.chain_id}_{user_id}', share)
                print(f"[Block {log['blockNumber']}] Event: {event['args']}")

            #RootStock Transfer
            logs = rs_w3.eth.get_logs({
                "fromBlock": last_btc_block + 1,
                "toBlock": current_btc_block,
                "address": rs_contract.address,
                "topics": [rs_transfer_filter_hash]
            })
            for log in logs:
                event = rs_transfer_filter().process_log(log)
                user_id = event['args'][f'user']
                share = event['args'][f'share{id}']
                receiver_id = event['args']['receiver']
                update_share(f'{rs_w3.eth.chain_id}_{user_id}', share, f'{rs_w3.eth.chain_id}_{receiver_id}')
                print(f"[Block {log['blockNumber']}] Event: {event['args']}")
            
            #RootStock Withdraw
            logs = rs_w3.eth.get_logs({
                "fromBlock": last_btc_block + 1,
                "toBlock": current_btc_block,
                "address": rs_contract.address,
                "topics": [rs_withdraw_filter_hash]
            })
            for log in logs:
                event = rs_withdraw_filter().process_log(log)
                user_id = event['args'][f'user']
                share = event['args'][f'share{id}']
                update_share_withdraw(f'{rs_w3.eth.chain_id}_{user_id}', share)
                print(f"[Block {log['blockNumber']}] Event: {event['args']}")
            last_btc_block = current_btc_block

        except Exception as e:
            print(f"Error: {e}")

    print("ETH-BLOCK", current_eth_block)
    print("BTC-BLOCK", current_btc_block)
    time.sleep(10)
