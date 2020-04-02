from modules.loadData import readData


def setupQuestion(number, choices):

    question = readData("questions")[number - 1]
    question = [question]
    question[0]['choices'] = choices
    return question