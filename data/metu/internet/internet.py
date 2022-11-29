internet_questions = {}



def add(question, answer):
    internet_questions[question] = answer
def remove(question):
    internet_questions.pop(question)
def replace(question, newanswer):
    internet_questions[question] = newanswer

def answer(question):
    if type(internet_questions[question]) != int:
        return internet_questions[question]
    else:
        fetch(internet_questions[question])

def fetch(qi): #qi = question index
    return