from modules.searchJSON import (findComponent, getDeviceNames, printComponent)
from modules.loadData import readData
from requests import get
from json import (loads, dumps)
from PyInquirer import prompt
from examples import custom_style_2


def main():
    res = get('http://localhost:5000/rest/firmware').json()
    uids = loads(findComponent(res, "uids")[0])["uids"]
    device_names = getDeviceNames(uids)

    question = readData("questions")[0]
    question = [question]
    question[0]['choices'] = device_names
    answers = prompt(question, style=custom_style_2)
    #answers = prompt(question, style=custom_style_2)


if __name__ == '__main__':
    main()
