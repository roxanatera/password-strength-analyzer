import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def generate_salt():
    return os.urandom(16)


def derive_key(master_password, salt, iterations=600000):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    key = kdf.derive(master_password.encode('utf-8'))
    return key

def encrypt(data, key):
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, data.encode('utf-8'), None)
    return {'nonce': nonce.hex(), 'ciphertext': ciphertext.hex()}

def decrypt(encrypted_data, key):
    aesgcm = AESGCM(key)
    nonce = bytes.fromhex(encrypted_data['nonce'])
    ciphertext = bytes.fromhex(encrypted_data['ciphertext'])
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode('utf-8')
