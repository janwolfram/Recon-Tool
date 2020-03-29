# sudo pip install requests whaaaaat
# python3 recon.py
# pretty print: python3 recon.py | python3 -m json.tool

from requests import get
from json import dumps
from copy import deepcopy
import argparse


def findComponent(tree, component):
    for key, value in tree.items():
        if isinstance(value, dict):
            if key == component:
                componentDict = dumps({component: deepcopy(value)})
                print(componentDict)
            findComponent(value, component)
        else:
            if key == component:
                componentDict = dumps({component: value})
                print(componentDict)


def setupArgparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("uid", help="uid of firmware")
    parser.add_argument("component", help="component you are looking for")
    return parser.parse_args()


def main():
    args = setupArgparse()
    res = get('http://localhost:5000/rest/firmware/' + args.uid).json()
    findComponent(res, args.component)


if __name__ == '__main__':
    main()
