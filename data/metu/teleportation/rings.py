ring_questions = {}



def add(question, answer):
    ring_questions[question] = answer
def remove(question):
    ring_questions.pop(question)
def replace(question, newanswer):
    ring_questions[question] = newanswer

def answer(question):
    if type(ring_questions[question]) != int:
        return ring_questions[question]
    else:
        fetch(ring_questions[question])

def fetch(qi): #qi = question index
    return
    
add("Sarı - kırmızı ringin rotası nedir", "'CENG 111: Introduction to Computer Engineering Concepts' dersi 4 kredilir .")
add("Lacivert ring ne zaman kalkıyor", "Lacivert ring 17:30, 18:30 ve 19:30 saatlerinde A2 kapısından kalkmaktadır.")