from json import loads


def loadData(file):
    with open('files/' + file) as f:
        return [element.rstrip() for element in f.readlines() if element != '']


def loadQuestions(file):
    with open('files/' + file) as f:
        return [loads(element) for element in f.readlines() if element != '']
