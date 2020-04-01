from modules.searchJSON import (findComponent, printComponent)
from requests import get


def main():
    res = get('http://localhost:5000/rest/firmware').json()


if __name__ == '__main__':
    main()
