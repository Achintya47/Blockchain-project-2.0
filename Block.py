from time import time
from Utility.Hasher import Hasher
import json
import socket
from Mining import Mine
import multiprocessing

class Block:
    def __init__(self,prev_hash,block_index,transactions,mine_block=1):
        self.transactions=list(transactions)
        self.prev_hash=prev_hash
        self.nonce=0
        self.mining_node="192.168.1.1"
        self.block_index=block_index
        # self.timestamp=time()
        self.merkleroot=self.merkle_calculate()
        self.blockhash=""
        if mine_block:
            multiprocessing.Process(target=Mine,args=(self,)).start()
    
    def merkle_calculate(self):        
        current_level =[tx if isinstance(tx, dict) else 
                         json.loads(tx) for tx in self.transactions]
        
        while len(current_level)>1:
            next_level=[]
            for i in range(0,len(current_level),2):
                if i+1<len(current_level):
                    hashpair=current_level[i]['Transaction Hash'] + current_level[i+1]['Transaction Hash']
                else:
                    hashpair=current_level[i]['Transaction Hash'] + current_level[i]['Transaction Hash']
                hash=Hasher(hashpair)
                next_level.append({'Transaction Hash':hash})
            current_level=next_level

        return current_level[0]
        
    def to_dict(self):
        return {
            'Label' : 'Block',
            'Mining Node':self.mining_node,
            'Block Hash':self.blockhash,
            'Block Index' : self.block_index,
            'Merkle Root':self.merkleroot,
            # 'Time Stamp':self.timestamp,
            'Nonce':self.nonce,
            'Previous Hash':self.prev_hash,
            'Transactions' : self.transactions}
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
    def host_block(self):
        node = "192.168.1.1"
        print("Entered Sender Code for node:", node)
        host = "192.168.1.255"  # Broadcast address
        message=json.dumps(self.to_dict(),indent=4)
        port = 12345
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Use UDP
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client_socket.sendto(message.encode(), (host, port))  # Send the string
        client_socket.close()
        print(f"Block Sent : {self.to_dict()}")
