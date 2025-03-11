from Utility.Hasher import Hasher
from time import time


class Transaction:
    def __init__(self,senderid,recieverid,amount):
        self.senderid=senderid
        self.timestamp=time()
        self.recieverid=recieverid
        self.amount=amount
        self.transactionhash=Hasher(f"{self.senderid} sends {self.recieverid} {self.amount}BTC at Time{self.timestamp}")
        
    def to_dict(self):
        return {'Label' : 'Transaction'
                ,'Sender ID' : self.senderid,
                'Reciever ID' : self.recieverid, 
                'Time Stamp' : self.timestamp,
                'Amount' : self.amount,
                'Transaction Hash' : self.transactionhash}
    