import os
import ecdsa
import binascii
import hashlib

if __name__ == '__main__':
    # hash
    print('### HASH ###')
    hash_hello = hashlib.sha256(b'Hello').hexdigest()
    print(hash_hello)

    hash_hello2 = hashlib.sha256(b'Hello World!').hexdigest()
    print(hash_hello2)
    
    # secret key
    print('')
    print('### SECRET KEY ###')
    private_key = os.urandom(32)
    public_key = ecdsa.SigningKey.from_string(
        private_key,
        curve=ecdsa.SECP256k1
    ).verifying_key.to_string()
    print(private_key)
    print(binascii.hexlify(private_key))
    print(binascii.hexlify(public_key))