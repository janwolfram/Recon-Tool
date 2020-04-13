import argparse
from requests import get
from modules.JSON import createReconJSON
from json import loads, dumps
from time import time
from modules.db import *
from termcolor import colored

from modules.prettyPrint import prettyPrint


def setupArgparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("uid", help="uid of firmware")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--interactive", help="start interactive-mode", action="store_true")
    group.add_argument("-j", "--json", help="print json", action="store_true")
    return parser.parse_args()


def main():
    start_first = time()
    args = setupArgparse()
    res = get('http://localhost:5000/rest/firmware/' + args.uid + '?summary=true').json()
    json = createReconJSON(res, args.uid)

    if args.json:
        print(dumps(json, indent=4, sort_keys=False))
    elif args.interactive:
        print('interactive')
    else:
        prettyPrint(json)

    print(f'Time taken: {time() - start_first}')


if __name__ == '__main__':
    main()
