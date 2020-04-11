from json import (dumps, loads)
from copy import deepcopy
from requests import get


def findComponent(t, c):
    out = []

    def findComponentInJson(tree, component):
        for key, value in tree.items():
            if isinstance(value, dict):
                if key == component:
                    out.append(dumps({component: deepcopy(value)}))
                else:
                    findComponentInJson(value, component)
            else:
                if key == component:
                    out.append(dumps({component: deepcopy(value)}))

    findComponentInJson(t, c)
    return out


def printComponent(components):
    for component in components:
        print(component)
        #print(dumps(loads(component), indent=0, sort_keys=True))
        print("\n")


def getDeviceNames(uids):
    device_names = []
    for uid in uids:
        device_name = getDeviceName(uid)
        device_names.append(device_name["device_name"])
    return device_names


def getDeviceName(uid):
    return loads(
        findComponent(get('http://localhost:5000/rest/firmware/' + uid).json(), "device_name")[0])


def getUid(device, uids):
    for uid in uids:
        if device == getDeviceName(uid)["device_name"]:
            return uid


def getcryptoUid(cryptoKeys, crypto, programsUids):
    for i, key in enumerate(cryptoKeys):
        if key == crypto:
            return programsUids[i][crypto]


def findCryptoMaterial(uid):
    return loads(
        findComponent(get('http://localhost:5000/rest/firmware/' + uid + "?summary=true").json(), "summary")[3])[
        "summary"]


def getProgramName(uid):
    return loads((findComponent(get('http://localhost:5000/rest/file_object/' + uid).json(), "hid"))[0])


def getCryptoKeys(summary_crypto):
    out = []
    for key in summary_crypto:
        out.append(key)
    return out


def getProgramsUids(summary_crypto):
    out = []
    for key in summary_crypto:
        value = loads(findComponent(summary_crypto, key)[0])[key]
        out.append({key: value})
    return out


def getCryptoMaterial(uid):
    return findComponent(get('http://localhost:5000/rest/file_object/' + uid).json(), "material")