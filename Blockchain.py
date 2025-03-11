import json
from Block import Block
from Utility.Hasher import Hasher
from Sender import send_message
import threading
import time
from Transaction import Transaction
import Reciever

class Blockchain():
    def __init__(self):
        self.chain=[]
        self.Genesis_block()

    def Genesis_block(self):
        print("BlockChain Has been Initiated")
        print("Genesis Block Initiated")
        genesis_block=Block(prev_hash="0",block_index=1,transactions=[{'Label':'Transaction',
        'Sender ID':'Achintya','Reciever ID':'Naman','Time Stamp':0,'Amount':45}],mine_block=0) 
        genesis_block.mining_node=""
        genesis_block.merkle_calculate()
        genesis_block.blockhash=Hasher(str(genesis_block.merkleroot) + 
                                  str(genesis_block.prev_hash) + str(genesis_block.nonce))
        self.chain.append(genesis_block)
        self.save_chain()

    def save_chain(self):
        with open("Blockchain.json",'w') as file:
            json.dump([block.to_dict() for block in self.chain],file,indent=4)
            # json.dump(self.to_dict(),file,indent=4)
                
    def add_block_self(self, new_block):
        self.chain.append(new_block)
        self.save_chain()


    
    # def __repr__(self):
    #     return str({'Label':'BlockChain',
    #                 'Blocks':[block.to_dict() for block in self.chain]})
        
Blockchain_event=Blockchain()

def main():
    from Reciever import Txn_list
    global Blockchain_event
    print("Welcome to the Blockchain")
    #Initialize the Reciever Module to run Forever
    Reciever_Thread=threading.Thread(target=Reciever.receive_message, daemon=True)
    Reciever_Thread.start()
    print("Reciever thread Active : ",Reciever_Thread.is_alive())    
    while True:
        choice=input("Do you want to Host a Transaction(Y/N) : ")
        if choice == "Y":
            senderid=input("Enter the Sender ID")
            recieverid=input("Enter the Reciever ID")
            amount=input("Enter the Amount")
            Txn=Transaction(senderid,recieverid,amount)
            
            message=json.dumps(Txn.to_dict(),indent=4)
            send_message(message)
            Txn_list.append(Txn.to_dict())
            if Reciever.mining:
                print("Mining in Process, Transaction in Buffer")
            else:
                if(len(Txn_list))>=5:
                    from Reciever import load_prev_info
                    Txn_list_copy=Txn_list
                    print("Transaction Limit Reached, Mining Block in main()")
                    previous_hash,last_index,blockchain=load_prev_info()
                    block_obj=Block(previous_hash,last_index + 1,Txn_list_copy)
                    Txn_list=Txn_list[5:]
                
                    # true_self_block=consensus(block_obj)
                    # if true_self_block:
                    # Blockchain_event.add_block_self(block_obj)
                    # block_obj.host_block()
                    # Txn_list.clear()
        else:
            time.sleep(1)


if __name__=="__main__":
    main()


    
        

