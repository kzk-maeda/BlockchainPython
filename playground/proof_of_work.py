import hashlib

class Block():
    def __init__(self, data, prev_hash):
        self.index = 0
        self.nonce = 0
        self.prev_hash = prev_hash
        self.data = data
    
    def blockhash(self):
        blockheader = str(self.index) + str(self.prev_hash) + str(self.data) + str(self.nonce)
        block_hash = hashlib.sha256(
            blockheader.encode()
        ).hexdigest()
        return block_hash
    
    def __str__(self):
        return "Block Hash : {} \nPrevious hash : {} \nIndex : {} \nData:".format(
            self.blockhash(),
            self.prev_hash,
            self.index,
            self.data
        )

class HashChain():
    def __init__(self):
        self.chain = ["000000000000000000000000000000000000000000"]
        