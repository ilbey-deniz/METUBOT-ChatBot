from catering import cafeteria
from dorms import dorms
from internet import internet
from departments import ceng
from teleportation import rings




def add_question(category, fl, q, a):
    if category == "catering":
        if fl == "cafeteria":
            cafeteria.add(q, a)
    if category == "dorms":
        if fl == "dorms":
            dorms.add(q, a)
    if category == "internet":
        if fl == "internet":
            internet.internet.add(q,a)
    if category == "teleportation":
        if fl == "rings":
            rings.add(q,a)
    if category == "departments":
        if fl == "ceng":
            ceng.add(q,a)

def answer_question(category, fl, q):
    if category == "catering":
        if fl == "cafeteria":
            return cafeteria.answer(q)
    if category == "departments":
        if fl == "ceng":
            return ceng.answer(q)
    

def admin_listener():
    #TODO: ADMINDEN KOMUT BEKLE
    ...

add_question("catering","cafeteria","Bugün yemekhanede ne yemek var", 1) #If the answer is a number, then we fetch the answer by calling fetch.
print(answer_question("catering","cafeteria","Bugün yemekhanede ne yemek var"))
add_question("departments","ceng","Müfredatta hangi dersler var", 1)
add_question("departments","ceng","111 dersi kaç kredili", "'CENG 111: Introduction to Computer Engineering Concepts' dersi 4 kredilir .")
add_question("departments","ceng","Data Structures neleri bağlıyor", "5710242, 5710315, 5710351, 5710350 .")
add_question("departments","ceng","Bölüm başkanı kimdir", "Halit S. Oğuztüzün")
add_question("departments","ceng","491 hangi ders", "CENG491 kodlu dersin adı Computer Engineering Design I' .")
print(answer_question("departments","ceng","Bölüm başkanı kimdir"))
print(answer_question("departments","ceng","Müfredatta hangi dersler var"))
