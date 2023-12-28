from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

def aes_encrypt(message, key):
    # Generate a random 16-byte Initialization Vector
    iv = os.urandom(16)

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_message = padder.update(message.encode()) + padder.finalize()

    # Create a Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    # Encrypt the plaintext
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()

    return iv + ciphertext

def aes_decrypt(ciphertext, key):
    # Get the Initialization Vector from the ciphertext
    iv = ciphertext[:16]

    # Create a Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    # Decrypt the ciphertext
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(ciphertext[16:]) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    message = unpadder.update(padded_message) + unpadder.finalize()

    return message.decode()

def generate_key():
    return os.urandom(32)

def store_key(key, name):
    os.environ[name] = key.hex()
    # if there is no .env file, create one
    if not os.path.exists('.env'):
        open('.env', 'w').close()
    # if the key is already in the .env file, remove it
    with open('.env', 'r') as f:
        lines = f.readlines()
    with open('.env', 'w') as f:
        for line in lines:
            if not line.startswith(name):
                f.write(line)

    # make it persistent
    with open('.env', 'a') as f:
        f.write(f'{name}={key.hex()}\n')

def get_key(name):
    if name in os.environ:
        return bytes.fromhex(os.environ[name])
    else:
        # read from .env file
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith(name):
                    return bytes.fromhex(line.split('=')[1])
                
def chacha20_encrypt(message, key):
    iv = os.urandom(16)

    cipher = Cipher(algorithms.ChaCha20(key, iv), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    return iv + ciphertext

def chacha20_decrypt(ciphertext, key):
    iv = ciphertext[:16]

    cipher = Cipher(algorithms.ChaCha20(key, iv), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()

    plaintext = decryptor.update(ciphertext[16:]) + decryptor.finalize()
    return plaintext.decode()