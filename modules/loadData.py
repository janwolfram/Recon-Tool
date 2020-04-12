from json import loads


def loadWhitelist():
    with open('files/whitelist') as f:
        return [element.rstrip() for element in f.readlines()]

