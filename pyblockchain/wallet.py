import base58
import codecs
import hashlib
import utils
from ecdsa import NIST256p
from ecdsa import SigningKey

class Wallet(object):

    def __init__(self):
        self._private_key = SigningKey.generate(curve=NIST256p)
        self._public_key = self._private_key.get_verifying_key()
        self._blockchain_address = self.generate_blockchain_address()

    @property
    def private_key(self):
        return self._private_key.to_string().hex()

    @property
    def public_key(self):
        return self._public_key.to_string().hex()

    @property
    def blockchain_address(self):
        return self._blockchain_address

    def generate_blockchain_address(self):
        #2
        public_key_bytes = self._public_key.to_string()
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        #3
        ripemd160_bpk = hashlib.new('ripemd160')
        ripemd160_bpk.update(sha256_bpk_digest)
        ripemd160_bpk_digest = ripemd160_bpk.digest()
        ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')
        #4
        network_byte = b'00'
        network_bitcoin_public_key = network_byte + ripemd160_bpk_hex
        network_bitcoin_public_key_bytes = codecs.decode(network_bitcoin_public_key, 'hex')
        #5
        sha256_bpk = hashlib.sha256(network_bitcoin_public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        sha256_2_bpk = hashlib.sha256(network_bitcoin_public_key_bytes)
        sha256_2_bpk_digest = sha256_2_bpk.digest()
        sha256_hex = codecs.encode(sha256_2_bpk_digest, 'hex')
        #6
        checksum = sha256_hex[:8]
        #7
        address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
        #8
        blockchain_address = base58.b58encode(address_hex).decode('utf-8')
        return blockchain_address
    

class Transaction(object):
    
    def __init__(self, sender_private_key, sender_public_key,
                sender_blockchain_address, recipient_blockchain_address, value):
        self.sender_private_key = sender_private_key
        self.sender_public_key = sender_public_key
        self.sender_blockchain_address = sender_blockchain_address
        self.recipient_blockchain_address = recipient_blockchain_address
        self.value = value
    
    def generate_signature(self):
        sha256 = hashlib.sha256()
        transaction = utils.sorted_dict_by_key({
            'sender_blockchain_address' : self.sender_blockchain_address,
            'recipient_blockchain_address' : self.recipient_blockchain_address,
            'value': float(self.value)
        })
        sha256.update(str(transaction).encode('utf-8'))
        message = sha256.digest()
        private_key = SigningKey.from_string(
            bytes().fromhex(self.sender_private_key), curve=NIST256p
        )
        private_key_sign = private_key.sign(message)
        signature = private_key_sign.hex()
        return signature







if __name__ == '__main__':
    wallet = Wallet()
    print(wallet.private_key)
    print(wallet.public_key)
    print(wallet.blockchain_address)

    transaction = Transaction(
        sender_private_key=wallet.private_key,
        sender_public_key=wallet.public_key,
        sender_blockchain_address=wallet.blockchain_address,
        recipient_blockchain_address='B',
        value=1.0
    )
    print(transaction.generate_signature())


