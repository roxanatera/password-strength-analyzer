import json
import os
from .crypto import generate_salt, derive_key, encrypt, decrypt

VAULT_FILE = 'vault.json'


def init_vault(master_password):
    salt = generate_salt()
    key = derive_key(master_password, salt)
    empty_list_json = json.dumps([])
    encrypted = encrypt(empty_list_json, key)
    vault_data = {
        'salt': salt.hex(),
        'nonce': encrypted['nonce'],
        'ciphertext': encrypted['ciphertext']
    }
    with open(VAULT_FILE, 'w') as f:
        json.dump(vault_data, f, indent=2)
    return vault_data


def unlock_vault(master_password):
    with open(VAULT_FILE, 'r') as f:
        vault_data = json.load(f)
    salt = bytes.fromhex(vault_data['salt'])
    key = derive_key(master_password, salt)
    encrypted_data = {
        'nonce': vault_data['nonce'],
        'ciphertext': vault_data['ciphertext']
    }
    plaintext = decrypt(encrypted_data, key)
    return json.loads(plaintext)


def save_vault(master_password, entries):
    with open(VAULT_FILE, 'r') as f:
        vault_data = json.load(f)
    salt = bytes.fromhex(vault_data['salt'])
    key = derive_key(master_password, salt)
    encrypted = encrypt(json.dumps(entries), key)
    vault_data['nonce'] = encrypted['nonce']
    vault_data['ciphertext'] = encrypted['ciphertext']
    with open(VAULT_FILE, 'w') as f:
        json.dump(vault_data, f, indent=2)
