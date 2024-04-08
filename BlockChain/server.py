import hashlib
import time
import json
import hmac
import random
from generate_prime import generate_large_prime
from flask import render_template,Flask,request
from threading import Thread

HMAC_KEY = b"secret"

app = Flask(__name__)

class Block:
    def __init__(self,prev_hash,transaction_list,proof) -> None:
        self.prev_hash = prev_hash
        self.transaction_list = transaction_list
        #Meta data
        self.nonce = 0
        self.proof = proof        
        self.timestamp = time.time()
        self.block_hash = self.get_hash()
    def get_hash(self):                
        block_string = json.dumps(self.to_dict(),sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    def __str__(self) -> str:
        return "Block Hash: {}\nPrevious Hash: {}\nProof: {}\nTransactions: {}\n".format(self.block_hash,self.prev_hash,self.proof,self.transaction_list)
    def mine_block(self,difficulty):
        while self.block_hash[:difficulty] != "0"*difficulty:
            self.nonce += 1
            self.block_hash = self.get_hash()
        # print("Block mined: ",self.block_hash)
        return self.block_hash
    def to_dict(self):
        transaction_list = []  
        for transaction in self.transaction_list:
            if(isinstance(transaction,Transaction)):
                transaction_list.append(transaction.to_dict())
            else:
                transaction_list.append(transaction)
        self.transaction_list = transaction_list
        return {
            "prev_hash": self.prev_hash,
            "transaction_list": self.transaction_list,
            "nonce": self.nonce,
            "proof": self.proof,
            "timestamp": self.timestamp,
        }
    
    
class Transaction:
    def __init__(self, buyer, seller, amount, land_size, land_location) -> None:
        self.buyer = buyer
        self.seller = seller
        self.amount = amount
        self.land_size = land_size
        self.land_location = land_location
        self.time = time.time()
        transaction_json = json.dumps(self.todict(), sort_keys=True)
        self.hmac = hmac.new(HMAC_KEY, transaction_json.encode(), hashlib.sha256).hexdigest()

    def to_string(self):
        return f"{self.buyer} paid {self.amount} to {self.seller} for a land of size {self.land_size} at {self.land_location}"

    def get_hmac(self, secret_key):
        return hmac.new(secret_key.encode(), str(self.__dict__).encode(), hashlib.sha256).hexdigest()

    def to_dict(self):
        return {
            "buyer": self.buyer,
            "seller": self.seller,
            "amount": self.amount,
            "land_size": self.land_size,
            "land_location": self.land_location,
            "time": self.time,
            "hmac": self.hmac
        }
    def todict(self):
        return {
            "buyer": self.buyer,
            "seller": self.seller,
            "amount": self.amount,
            "land_size": self.land_size,
            "land_location": self.land_location,
            "time": self.time,
        }
        
    def verifytransaction(self):
          verifier = Verifier(self)
          return verifier.verify()
       

class Verifier:
    def __init__(self,transaction) -> None:
        self.transaction = transaction
    def verify(self):
        expected_hmac = self.transaction.hmac
        transaction_json = json.dumps(self.transaction.todict(), sort_keys=True)
        computed_hmac = hmac.new(HMAC_KEY, transaction_json.encode(), hashlib.sha256).hexdigest()
        self.transaction.hmac = expected_hmac
        return expected_hmac == computed_hmac
        

class BlockChain:
    def __init__(self) -> None:
        self.chain = []
        self.unconfirmed_transactions = []
        self.users = []
        self.genesis_block()
    def genesis_block(self):
        transactions = []
        genesis_block = Block("0",transactions,0)
        genesis_block.block_hash = genesis_block.get_hash()
        self.chain.append(genesis_block)
    def create_block(self,proof):
        block = Block(self.chain[-1].block_hash,self.unconfirmed_transactions,proof)
        # print("Block created: ",block)
        self.unconfirmed_transactions = []
        block.mine_block(2)
        # print("Block mined: ",block)
        self.chain.append(block)
        # print(self.chain)
        return block
    def mine_pending_transactions(self,mining_reward_address):
        if len(self.unconfirmed_transactions) == 0:
            return None
        reward_transaction = Transaction("network",mining_reward_address,100," ","")
        self.unconfirmed_transactions.append(reward_transaction)
        last_block = self.chain[-1]
        return self.create_block(last_block.proof)
    def add_transaction(self,transaction):
        if transaction.verifytransaction() == True:
            self.unconfirmed_transactions.append(transaction)
        else:
            print("Transaction verification failed")
    def proof_of_work(self):
        last_proof = self.chain[-1].proof
        proof = 0
        while self.valid_proof(last_proof,proof) is False:
            proof += 1
        return proof
    def print_blocks(self):
        for block in self.chain:
            # print(block)
            print("\n")
    def view_users(self):
        for user in self.users:
            # print(user)
            print("\n")
    def user_transactions(self,user):
        transactions = []
        for block in self.chain:
            for transaction in block.transaction_list:
                if transaction["buyer"]== user or transaction["seller"] == user:
                    transactions.append(transaction)
        if len(transactions) ==0:
            for transact in self.unconfirmed_transactions:
                if transact.buyer == user or transact.seller == user:
                    return "Pending Transaction Wait for it to be mined"
            return None
        return transactions
        
    def make_transaction(self,buyer,seller,amount,land_size,land_location):
        transaction = Transaction(buyer,seller,amount,land_size,land_location)
        self.add_transaction(transaction)


def mine_indef(blockchain):
    while True:
        blockchain.mine_pending_transactions("Miner Address")
    
blocky = BlockChain()

@app.route("/")
def home():
    return render_template("index.html",message="")
@app.route("/addtransaction",methods=["POST"])
def add_transaction():
    buyer = request.form["Buyer"]
    seller = request.form["Seller"]
    amount = request.form["Price"]
    land_size = request.form["Size"]
    land_location = request.form["Location"]
    blocky.make_transaction(buyer,seller,amount,land_size,land_location)
    return render_template("index.html",message="Transaction added to Pending List. Waiting to be mined")
@app.route("/mine", methods=["GET"])
def mine():
    return render_template("mine.html",message="")
@app.route("/mineblock",methods=["POST"])
def mine_block():
    addr = request.form["address"]
    blocky.mine_pending_transactions(addr)
    return render_template("mine.html",message="Block mined successfully")
@app.route("/view",methods=["GET"])
def view():
    return render_template("view.html",message="")
@app.route("/viewchain",methods=["POST"])
def view_chain():
    user = request.form["user"]
    print(user)
    trans = blocky.user_transactions(user)
    print(trans)
    
    if trans == "Pending Transaction Wait for it to be mined":
        return render_template("view.html",message="Pending Transaction Wait for it to be mined")
    elif(trans is not None ):
        return render_template("view.html",message=(trans))
    else:
        return render_template("view.html",message="No transactions found for user")


@app.route("/viewuser", methods=["GET"])
def view_user():
    name = request.args.get('name')
    if name:
        trans = blocky.user_transactions(name)
        if trans == "Pending Transaction Wait for it to be mined":
            return render_template("view.html", message="Pending Transaction Wait for it to be mined")
        elif trans is not None:
            return render_template("view.html", message=trans)
        else:
            return render_template("view.html", message="No transactions found for user")
    else:
        return render_template("view.html", message="Please enter a name to search")


if(__name__ == "__main__"):
    thread = Thread(target=mine_indef,args=(blocky,),daemon=True)
    thread.start()
    app.run(debug=True)
    