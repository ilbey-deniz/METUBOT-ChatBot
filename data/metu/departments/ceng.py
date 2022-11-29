ceng_questions = {}



def add(question, answer):
    ceng_questions[question] = answer
def remove(question):
    ceng_questions.pop(question)
def replace(question, newanswer):
    ceng_questions[question] = newanswer

def answer(question):
    if type(ceng_questions[question]) != int:
        return ceng_questions[question]
    else:
        fetch(ceng_questions[question])

def fetch(qi): #qi = question index
    return
    
add("111 dersi kaç kredili", "'CENG 111: Introduction to Computer Engineering Concepts' dersi 4 kredilir .")
add("Data Structures neleri bağlıyor", "5710242, 5710315, 5710351, 5710350 .")
add("Bölüm başkanı kimdir", "Halit S. Oğuztüzün")
add("491 hangi ders", "CENG491 kodlu dersin adı Computer Engineering Design I' .")