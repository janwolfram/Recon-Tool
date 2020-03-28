# sudo pip install requests
# python3 recon.py
# pretty print: python3 recon.py | python3 -m json.tool

import requests
import json
import copy


def FindComponent(tree, component): 
    for key, value in tree.items():
        if isinstance(value, dict):
            if key == component:
                componentDict = json.dumps({component : copy.deepcopy(value)})
                print(componentDict)
            FindComponent(value, component)
        else:
            if key == component:
                componentDict = json.dumps({component : value})
                print(componentDict)


def main():
    res = requests.get('http://localhost:5000/rest/firmware/950f6f50fa2a16295193a9586bf6795b722805ab32099f5631f35b3fc717ce1b_33228800').json()
    FindComponent(res, "analysis")


if __name__ == '__main__':
    main()

