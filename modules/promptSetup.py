from modules.loadData import loadQuestions


def setupQuestion(number, choices):
    question = loadQuestions("questions")[number - 1]
    question = [question]
    question[0]['choices'] = choices
    return question