#!/usr/bin/env python
import binascii
import itertools
from pyDes import des


# Instructions
# * Use the skeleton code provided here.
# * Use the DES library as shown in twodes.py
# * Use binascii's (un)hexlify to convert between bytes and hex
#   representation. We do not care if you do your comparisons on bytes
#   or hex - in our sample solution we have chosen hex for better
#   readability of debugging output. The only thing we require is that
#   the "ciphertext" input to lookupInTable() is in hex.
# * In your final solution, your last two lines that you print to the
#   screen MUST be the output of lookupInTable, exactly in the format
#   indicated!

# The following is your plaintext/ciphertext pair.
plaintext = "acknowledgements"   # <- plaintext goes here
ciphertext = "e1616415d9cb2da29e559042edae3672"  # <- ciphertext goes here

# Read in the effective keylength in number of hex digits. This value
# is either 3 or 4 in our case:
effKeyLength = 4

# the function handed to us to get the decryption done
def twodes(plain, keyOne, keyTwo):
    cipherOne = des(binascii.unhexlify(keyOne), pad=None)
    cipherTwo = des(binascii.unhexlify(keyTwo), pad=None)
    return cipherTwo.encrypt(cipherOne.encrypt(plain))


# This function generates and returns the total number of keys that could have been used
def generatePermutation():
    t = ["".join(seq) for seq in itertools.product("0123456789abcdef", repeat=effKeyLength)]
    for x in t:
        yield x


# function to check and give the corrct padding
def checkPad(effKeyLength):
    # default pad 16 hex digit
    def_pad = "0000000000000000"
    if (effKeyLength > 4):
        # since the test scope is out of the condition print the warning
        print "Key Length greater than 4 will take much time"
    return def_pad[0:-(effKeyLength)]


# Generate the "forward" table
# Input: plaintext in hex, effective key length in hex digits
# (3 or 4, see above)
# Don't forget to use the IV (see above)
# Output: a representation of the forward table
def generateTable(plaintext, effKeyLength):
    # Call generate Permutation to yield all the possible combinations of key length
    perms = generatePermutation();
    # Check for the correct padding accoding to keylength
    pad = checkPad(effKeyLength);
    # initialize the dictionary to hold the values
    enctable = {}
    # Loop thorugh all possible keys
    for p in perms:
        # pad the possible keys to make it 16 Hex digit
        p = pad + p
        if (len(p) != 16):
            # Some logic has gone wrong
            print "padding gone wrong..."
        # Initate the key for single DES encryption
        k1 = des(binascii.unhexlify(p), pad=None)
        # yield p+":"+binascii.hexlify(k1.encrypt(plaintext))

        # store the key, value pair for further inspection
        enctable[p] = binascii.hexlify(k1.encrypt(plaintext))
    return enctable


# return true if the guessed key pair gives correct ciphertext for the plaintext
def checkCipher(x, p):
    # Call the twodes function to check if the ciphertext is produced by the guess key values
    if (ciphertext == binascii.hexlify(twodes(plaintext, x, p))):
        return True
    return False


# Do the lookups.
# Input:
# * the representation of your forward table
# * the ciphertext as hex representation
# * the effective key length
# Don't forget to use the IV if you do crypto here (see above)
# Output:
# Key 1, Key 2 in *exactly* the format as below
def lookupInTable(enctable, ciphertext, effKeyLength):
    # the return variables
    key1, key2 = "", ""
    # repeat the first initialization step as in encryption
    # Call generate Permutation to yield all the possible combinations of key length
    perms2 = generatePermutation();
    # Check padding
    pad = checkPad(effKeyLength)
    # Set the flag false for matched keys
    flag = False
    for p in perms2:
        # pad the possible keys to make it 16 Hex digit
        p = pad + p
        if (len(p) != 16):
            # Some logic has gone wrong
            print "padding gone wrong..."
            return
        # Initialize the key for decryption
        k2 = des(binascii.unhexlify(p), pad=None)
        # decrypt the ciphertext
        pt = binascii.hexlify(k2.decrypt(binascii.unhexlify(ciphertext)))

        # Loop through lookup table
        for x in enctable:
            if (enctable[x] == pt):
                # If match is found do the final check for ciphertext and keypairs
                if checkCipher(x, p):
                    # Set the flag true,assing the keys, break the loop
                    flag = True
                    key1 = x
                    key2 = p
                    break
        # since the task is done break the loop
        if flag:
            break
    print "Key1:" + key1
    print "Key2:" + key2


# Start of main function
def main():
    print "Finding the keys used to encrypt", plaintext, "into", ciphertext
    print "This process will take some time ..."
    enctable = generateTable(plaintext, effKeyLength)
    lookupInTable(enctable, ciphertext, effKeyLength)


#main()
print(twodes("e1616415d9cb2da29e559042edae367244a184c7b76e77b141d318fa7b8ae3be3b81fe7e1bc74e649b8438811e3123df27c7627c253be4deb38d65f5117b9e93381cd7ffe82dd2656bd10e78cb28d21dc21acc5ec5a14d8347b4834c169b89545cfc81ca29e8702485cc33ea1d28f020dd6ce3bef3674b7a26178d32ebbd0ea514984f5ed35689c546f4b87c6c4fe4a44b6257a63d422ac3883ad95e25571671a598b2a6f104748ae1616415d9cb2da2d8f73c9c4df5099cf6e2ef1251fbf1768379179c86dafce2dd2f3a0c9cb617effc7ba68030478423012f856ca3c983f2a979580844f22f8e2867da2b8959d4c2f54dae219dde7daa47d90a2a80dedbe74428d2d601f79db0a393de5daecbd64fc7da6ce109577ee210fa7890329522f70b013e29586445d9d1f0970124e53fbe59651cf7003ee29b","000000000000001b","0000000000000052"))