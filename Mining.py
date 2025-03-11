from Utility.Hasher import Hasher
import Reciever  # Import module, not variable


difficulty = 6

def Mine(Block, difficulty=6):
    from Blockchain import Blockchain_event
    nonce = 0
    blockhash = ""
    Reciever.mining=True

    while Reciever.mining:  # Access latest value dynamically
        blockhash = Hasher(str(Block.merkleroot) + str(Block.prev_hash) + str(nonce))
        
        if blockhash[:difficulty] == "0" * difficulty:
            print(f"\nBlock Mined! Nonce: {nonce}, Hash: {blockhash}")                
            Block.blockhash = blockhash
            Block.nonce = nonce
            Blockchain_event.add_block_self(Block)
            Block.host_block()
            Reciever.mining=False
            return 1  # Successfully mined block
        nonce += 1
        # print(f"Mining Block {Block.block_index}, Nonce: {nonce}", end="\r")

    print("\nAnother Valid Block Received, Stopping Mining") 
    return 0  # Mining stopped due to another block



# from Utility.Hasher import Hasher

# import Reciever
# #stop_mining is a variable, updated in the reciever module

# difficulty=7

# def Mine(Block,difficulty=7):
#     nonce=0
#     blockhash=""
#     while True:
#         if mining:
#             blockhash = Hasher(str(Block.merkleroot) + str(Block.prev_hash)
#                             + str(nonce))
#             if blockhash[:difficulty] == "0" * difficulty:
#                 print(f"Block Mined! Nonce: {nonce}, Hash: {blockhash}")                
#                 break
#         else:
#             print("Another Valid Block Recieved,Stop Mining") 
#             break
#         nonce+=1
#         blockhash=""
#         print(f"Mining Block : {Block.block_index} for Nonce Value: {nonce}", end="\r")

#     if mining:
#         Block.blockhash=blockhash
#         Block.nonce=nonce
#         return 1
#     else:
#         return 0

