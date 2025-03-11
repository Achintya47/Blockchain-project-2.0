import socket
import threading
import json
from Utility.Hasher import Hasher


#Buffer for Transactions made during Mining process
mining=False

difficulty=6
Txn_list=[]
buffer=""

def load_prev_info():

    '''Returns the Previous hash and Index of Last Block from the json'''
    with open("Blockchain.json") as file:
        file.seek(0)
        blockchain=json.load(file)
        last_block=blockchain[-1]
        previous_hash=last_block['Block Hash']
        last_index=last_block['Block Index']
        return previous_hash,last_index,blockchain

def receive_message():

    """Continuously listens for incoming JSON-formatted strings and stops mining if a block is received"""
    host = "0.0.0.0"  # Listen on all available network interfaces
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow immediate reuse of the socket
    server_socket.bind((host, port))
    my_ip="192.168.1.1"
    

    print(f"\nUDP Server listening on {host}:{port}\n")

    while True:  # Keep server running forever
        data, addr = server_socket.recvfrom(4096)  # Accept a new connection
        sender_ip,_=addr
        print("My ip:" ,my_ip,"Sender IP: ",sender_ip)
        if sender_ip==my_ip:
            print("Self hosted message ignored")
            continue
        else:
            print(f"Recieved data from {addr}")
            threading.Thread(target=handle_client, args=(data,)).start()  # Handle each client in a new thread


def handle_client(data):
    from Blockchain import Blockchain_event
    global Txn_list,mining

    '''Handle incoming JSON-formatted string messages from a connected client'''
    # try:
    message=data.decode().strip()  # Receive, decode, and clean string
    print(f"\nRecieved Raw Message : {message}")
    
    try:
        message = json.loads(message)  # Convert string to dictionary
    except json.JSONDecodeError:
        print("Invalid JSON format received. Ignoring message.")
        return

    if message.get("Label") == "Block":
        print("Block Recieved, Consensus runnning")
        rec_block=jsontoblock(message)
        true_rec_block=consensus(rec_block)
        if true_rec_block:
            print("Valid Block, adding it to the chain")
            Blockchain_event.add_block_self(rec_block)
        else:
            print("Invalid Block Recieved")

    elif message.get("Label")=="Transaction":
        #While mining, transactions are added to the buffer
        print("Recieved a Transaction, adding it to the current list")        
        Txn_list.append(message)

        if mining:
            print("Mining in Process, Transaction in Buffer")  
        else:
            from Block import Block
            Txn_list.append(message)                
            if (len(Txn_list)>=5):
                print("Transaction Limit Reached, Mining Block")
                previous_hash,last_index,blockchain=load_prev_info()
                block_obj=Block(previous_hash,last_index + 1,Txn_list[:5])
                Txn_list=Txn_list[5:]
                true_self_block=consensus(block_obj)
                # if true_self_block:
                #     Blockchain_event.add_block_self(block_obj)
                #     block_obj.host_block()
                # else:
                #     print("Block Incorrectly Mined")
        
            

def jsontoblock(message):
    from Block import Block
    block_obj=Block(message['Previous Hash'],message['Block Index'],message['Transactions'],mine_block=0)
    block_obj.blockhash=message['Block Hash']
    block_obj.nonce=message['Nonce']
    block_obj.merkleroot=message['Merkle Root']
    block_obj.mining_node=message['Mining Node']
    # block_obj.timestamp=message['Time Stamp']
    return block_obj


#Here merkle root verification still needs to be implemented
def consensus(Block):
    '''Consensus itself calls the blockchain, the previous block's hash and the index,
    why? because this consensus will be used in the mining module as well when the miner has
    mined the block'''
    global mining
    
    prev_hash,last_index,blockchain=load_prev_info()
    blockhash=Hasher(str(Block.merkleroot) + str(Block.prev_hash)
                                    + str(Block.nonce))
    hash_verify=(blockhash[:difficulty]=="0"*difficulty)
    prev_verify=(Block.prev_hash==prev_hash)
    
    if(hash_verify and prev_verify):
        if mining:
            mining=False
            print("Mining was in process, mining now stopped")
        print("Block Valid")
        return 1

    else:
        print("\nInvalid Block, Continue Mining\n")
        return 0