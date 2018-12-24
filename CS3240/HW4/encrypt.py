#Gabriel Groover(gtg3vv)
#Homework 4, pycrypto

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import ARC4


def secret_string(string, key):
    return key.encrypt(string.encode(),32)[0]

def enc_file(file, key):
    cipher = ARC4.new(key)
    try:
        with open(file,'rb') as r:
            with open(file+".enc",'wb') as w:
                for line in r:
                    w.write(cipher.encrypt(line))
                return True
    except FileNotFoundError:
        print("File Name Incorrect")
        
    return False
    
def decrypt_file(file, key):
    cipher = ARC4.new(key)
    try:
        with open(file, 'rb') as r:
            with open('DEC'+file[:-4],'wb') as w:
                for line in r:
                    w.write(cipher.decrypt(line))
                return True
    except FileNotFoundError:
        print('File Name Incorrect')
        
    return False
