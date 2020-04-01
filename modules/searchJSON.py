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
        print(dumps(loads(component), indent=4, sort_keys=True))


def getDeviceNames(uids):
    device_names = []
    for uid in uids:
        device_name = getDeviceName(uid)
        device_names.append(device_name["device_name"])
    return device_names


def getDeviceName(uid):
    return loads(
        findComponent(get('http://localhost:5000/rest/firmware/' + uid).json(), "device_name")[0])

