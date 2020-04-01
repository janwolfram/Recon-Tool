from json import loads


def readData(file):
    with open('files/' + file) as f:
        data_list = f.readlines()
        for i, data in enumerate(data_list):
            data_list[i] = loads(data_list[i])
        return data_list
