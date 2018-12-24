__author__ = 'horton'

import os
from Crypto.Hash import SHA256
from Crypto.Hash import MD5

# Example 1: SHA-256
print(SHA256.new(b'abc').hexdigest())


# Example 2: Applications, hashing passwords
# Note: this demonstrates the idea, but there are modules that do this better

stored_hashes = { b'my-password' : '6fa2288c361becce3e30ba4c41be7d8ba01e3580566f7acc76a7f99994474c46' }
def check_password(clear_password, password_hash):
    return SHA256.new(clear_password).hexdigest() == password_hash

password_entered = b'my-password'
result = check_password(password_entered, stored_hashes[password_entered])
print("hashes match?", result)


# Example 2: Applications, file checksum
def get_file_checksum(filename):
    h = MD5.new()
    chunk_size = 8192
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if len(chunk) == 0:
                break
            h.update(chunk)
    return h.hexdigest()

print("Calculated MD5 checksum for file pycrypto1.py:", get_file_checksum("pycrypto1.py")) # we know this file exists! :-)