from modules.searchJSON import (findComponent, getDeviceNames, findCryptoMaterial, getUid, printComponent,
                                getProgramName, getcryptoUid, getProgramsUids, getCryptoKeys, getCryptoMaterial)
from modules.loadData import readData
from requests import get
from json import (loads, dumps)
from PyInquirer import prompt
from examples import custom_style_2
from modules.promptSetup import setupQuestion
from base64 import b64decode
from time import time
import faster_than_requests as requests
from tinydb import TinyDB


def main():
    '''
    start_first = time()
    res = get(
        'http://localhost:5000/rest/firmware/fb24a94d4f4057befbcefd1ae7ffb0a78a9b94aaa091bc17ed1d55ee594a3063_11046120?summary=true').json()
    test = loads(findComponent(res, "unpacked")[0])["unpacked"]
    count = 0

    db = TinyDB('fb24a94d4f4057befbcefd1ae7ffb0a78a9b94aaa091bc17ed1d55ee594a3063_11046120.json')
    table = db.table("unpacked")
    
    for i, element in enumerate(test):
        program = get('http://localhost:5000/rest/binary/' + test[i]).json()
        filename = program["file_name"]
        binary = program["binary"]
        table.insert({"file_name": filename, "binary": binary})
        print(i)
    
    for row in table:
        test2 = row["binary"]
        test2 = b64decode(test2)
        test2 = str(test2)
        if test2.count("smbd") > 0:
            print(row["file_name"])
            count = count + 1
    print(count)
    print(f'Time taken: {time() - start_first}')
    # print("break")
    start_second = time()
    
    for j, test in enumerate(table):
        test2 = loads(findComponent(test, "binary")[0])["binary"]
        test2 = b64decode(test2)
        test2 = str(test2)
        print(j)
        if test2.count("lighttpd") > 0:
            count = count + 1
    print(f'Time taken: {time() - start_second}')
    print(count)
'''

    res = get('http://localhost:5000/rest/firmware').json()
    uids = loads(findComponent(res, "uids")[0])["uids"]
    device_names = getDeviceNames(uids)

    question = setupQuestion(1, device_names)
    answers = prompt(question, style=custom_style_2)

    currentDevice = answers["firmware"]
    currentUid = getUid(currentDevice, uids)

    question = setupQuestion(2, ["crypto_material", "network-software/server"])
    answers = prompt(question, style=custom_style_2)

    if answers["analysis"] == "crypto_material":
        summary_crypto = findCryptoMaterial(currentUid)
        cryptoKeys = getCryptoKeys(summary_crypto)
        programsUids = getProgramsUids(summary_crypto)

        question = setupQuestion(3, cryptoKeys)
        answers = prompt(question, style=custom_style_2)

        currentCrypto = answers["crypto_material"]
        currentUids = getcryptoUid(cryptoKeys, currentCrypto, programsUids)

        programNames = []
        for program in currentUids:
            programNames.append(getProgramName(program)["hid"])

        question = setupQuestion(4, programNames)
        answers = prompt(question, style=custom_style_2)

        file = answers["crypto_file"]
        for i, name in enumerate(programNames):
            if file == name:
                materials = getCryptoMaterial(currentUids[i])

        test = loads(materials[0])["material"]
        choiceMaterial = []
        for i, material in enumerate(test):
            choiceMaterial.append("material " + str(i))

        question = setupQuestion(5, choiceMaterial)
        answers = prompt(question, style=custom_style_2)

        activeMaterial = answers["material"]
        test1 = activeMaterial.split()[1]
        test1 = int(test1)

        print(test[test1])



if __name__ == '__main__':
    main()
