import binascii
from pyDes import des

#the function handed to us to get the encryption done
def twoDES_encryption(plain, keyOne, keyTwo):
    cipherOne = des(binascii.unhexlify(keyOne), pad=None)
    cipherTwo = des(binascii.unhexlify(keyTwo), pad=None)
    return cipherTwo.encrypt(cipherOne.encrypt(plain))

#the function handed to us to get the decryption done
def twoDES_decryption(cipher, keyOne, keyTwo):
    cipherOne = des(binascii.unhexlify(keyOne), pad=None)
    cipherTwo = des(binascii.unhexlify(keyTwo), pad=None)
    return cipherOne.decrypt(cipherTwo.decrypt(cipher))


#Start of main function
def main():

    message = "e1616415d9cb2da29e559042edae367244a184c7b76e77b141d318fa7b8ae3be3b81fe7e1bc74e649b8438811e3123df27c7627c253be4deb38d65f5117b9e93381cd7ffe82dd2656bd10e78cb28d21dc21acc5ec5a14d8347b4834c169b89545cfc81ca29e8702485cc33ea1d28f020dd6ce3bef3674b7a26178d32ebbd0ea514984f5ed35689c546f4b87c6c4fe4a44b6257a63d422ac3883ad95e25571671a598b2a6f104748ae1616415d9cb2da2d8f73c9c4df5099cf6e2ef1251fbf1768379179c86dafce2dd2f3a0c9cb617effc7ba68030478423012f856ca3c983f2a979580844f22f8e2867da2b8959d4c2f54dae219dde7daa47d90a2a80dedbe74428d2d601f79db0a393de5daecbd64fc7da6ce109577ee210fa7890329522f70b013e29586445d9d1f0970124e53fbe59651cf7003ee29b" # message must be a multiple of 8 bytes in length

    ### UNCOMMENT THE FOLLOWING LINE IF YOU ARE DECRYPTING A HEX MESSAGE (ciphertext)
    message = binascii.unhexlify(message)

    key1 = "000000000000001b"  # key must be 8 bytes in length
    key2 = "0000000000000052"  # key must be 8 bytes in length

    ### RUN THE FOLLOWING BLOCK FOR ENCRYPTION
    #ciphertext = twoDES_encryption(message, key1, key2)
    #print("The ciphertext is:\t", binascii.hexlify(ciphertext))

    ### RUN THE FOLLOWING BLOCK FOR DECRYPTION
    plaintext = twoDES_decryption(message, key1, key2)
    print("The plaintext is:\t", plaintext)


if __name__ == "__main__":
    main()