import base64
from modules.requestFunctions import getBinary


def printBinary(tree):
    binary = getBinary(tree)
    binary_dec = base64.b64decode(binary)
    binary_dec = binary_dec.decode("cp437")
    print(binary_dec)
