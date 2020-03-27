# sudo pip install requests
# python3 recon.py

import requests
import pprint


def main():
    res = requests.get('http://localhost:5000/rest/firmware/950f6f50fa2a16295193a9586bf6795b722805ab32099f5631f35b3fc717ce1b_33228800')

    res = res.json()
    pp = pprint.PrettyPrinter(indent=0, width=80, depth=None)
    pp.pprint(res)
    #print(res)


    # hier kommt rekursive funktion um dict tiefgehend durchzugehen
    '''for key, value in res.items():
        print(key, value)
        print("\n")
    '''

if __name__ == '__main__':
    main()

