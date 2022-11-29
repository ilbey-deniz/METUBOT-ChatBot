dorm_questions = {}



def add(question, answer):
    dorm_questions[question] = answer
def remove(question):
    dorm_questions.pop(question)
def replace(question, newanswer):
    dorm_questions[question] = newanswer

def answer(question):
    if type(dorm_questions[question]) != int:
        return dorm_questions[question]
    else:
        return fetch(dorm_questions[question])

def fetch(qi): #qi = question index
    return
    
add("Batı yurtları hangileridir", "Batı yurtları; 19.Yurt, Faika Demiray, İsa Demiray ve Refika Aksoy olmak üzere 4 tanelerdir .")
add("Batı yurtları kaç tanedir", "Batı yurtları; 19.Yurt, Faika Demiray, İsa Demiray ve Refika Aksoy olmak üzere 4 tanelerdir .")
add("Doğu yurtları hangileridir", "Doğu yurtları; 1-9. Yurtlar olmak üzere 9 tanelerdir .")
add("Doğu yurtları kaç tanedir", "Doğu yurtları; 1-9. Yurtlar olmak üzere 9 tanelerdir .")
