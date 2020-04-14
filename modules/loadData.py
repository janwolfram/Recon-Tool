from json import loads


def loadData(file):
    with open('files/' + file) as f:
        return [element.rstrip() for element in f.readlines() if element != '']


def loadQuestions(file):
    with open('files/' + file) as f:
        data_list = f.readlines()
        for i, data in enumerate(data_list):
            data_list[i] = loads(data_list[i])
        return data_list
