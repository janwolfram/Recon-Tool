import argparse
from requests import get
from modules.Binary import printBinary
from modules.JSON import createReconJSON
from json import dumps
from time import time
from modules.interactive import startInteractive
from modules.prettyPrint import prettyPrint
from modules.requestFunctions import getFirmwareUids


def setupArgparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("uid", help="uid of firmware")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--interactive", help="start interactive-mode", action="store_true")
    group.add_argument("-j", "--json", help="print json", action="store_true")
    group.add_argument('-b', '--binary', help="print binary of file_objet", action="store_true")

    return parser.parse_args()


def setupJSON(uid):
    res = get('http://localhost:5000/rest/firmware/' + uid + '?summary=true').json()
    return createReconJSON(res, uid)


def isFirmware(arguid, uids):
    for uid in uids:
        if uid == arguid:
            return True


def main():
    start_first = time()
    args = setupArgparse()
    uids = getFirmwareUids(get('http://localhost:5000/rest/firmware').json())

    if args.json and isFirmware(args.uid, uids):
        json = setupJSON(args.uid)
        print(dumps(json, indent=4, sort_keys=False))
        print(f'Time taken: {time() - start_first}')
    elif args.interactive and isFirmware(args.uid, uids):
        json = setupJSON(args.uid)
        startInteractive(json)
    elif args.binary and isFirmware(args.uid, uids) is None:
        binaryRes = get('http://localhost:5000/rest/binary/' + args.uid).json()
        printBinary(binaryRes)
    elif not args.binary:
        json = setupJSON(args.uid)
        prettyPrint(json)
        print(f'Time taken: {time() - start_first}')


if __name__ == '__main__':
    main()
