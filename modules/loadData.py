from json import loads


def readData(file):
    with open('files/' + file) as f:
        data_list = f.readlines()
        for i, data in enumerate(data_list):
            data_list[i] = loads(data_list[i])
        return data_list


def readWhitelist():
    with open('files/whitelist') as f:
        data_list = f.readlines()
        for i, line in enumerate(data_list):
            data_list[i] = line.rstrip()
        return data_list
