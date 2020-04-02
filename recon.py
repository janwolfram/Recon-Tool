from modules.searchJSON import (findComponent, getDeviceNames, findCryptoMaterial, getUid, printComponent,
                                getProgramName, getcryptoUid, getProgramsUids, getCryptoKeys, getCryptoMaterial)
from modules.loadData import readData
from requests import get
from json import (loads, dumps)
from PyInquirer import prompt
from examples import custom_style_2
from modules.promptSetup import setupQuestion


def main():
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

    if answers["analysis"] == "network-software/server":
        test = findComponent(get('http://localhost:5000/rest/firmware/' + currentUid + "?summary=true").json(), "summary")[6]
        print(dumps(loads(test), indent=4, sort_keys=True))
        print(currentDevice)


if __name__ == '__main__':
    main()
