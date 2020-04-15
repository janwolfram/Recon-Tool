import base64
import pprint

from modules.requestFunctions import getBinary


def printBinary(tree):
    binary = getBinary(tree)
    binary_dec = base64.b64decode(binary)
    binary_str = binary_dec.decode("cp437")
    print(binary_str)
