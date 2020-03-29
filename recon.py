# sudo pip install requests
# python3 recon.py
# pretty print: python3 recon.py | python3 -m json.tool

from requests import get
from json import dumps
from copy import deepcopy
import argparse


def findComponentInJson(t, c):
    out = {}

    def findComponent(tree, component):
        for key, value in tree.items():
            if isinstance(value, dict):
                if key == component:
                    out["content"] = dumps({component: deepcopy(value)})
                else:
                    findComponent(value, component)
            else:
                if key == component:
                    out["content"] = dumps({component: value})

    findComponent(t, c)
    return out["content"]


def setupArgparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--uid", help="uid of firmware", required=False)
    parser.add_argument("-c", "--component", help="component you are looking for", required=False)
    return parser.parse_args()


def main():
    args = setupArgparse()
    if args.uid and args.component:
        res = get('http://localhost:5000/rest/firmware/' + args.uid).json()
        print(findComponentInJson(res, args.component))
    else:
        res = get('http://localhost:5000/rest/firmware').json()
        print(findComponentInJson(res, "uids"))


if __name__ == '__main__':
    main()
