from catering import cafeteria
import dorms
import internet
import departments
import teleportation
import os




def add_question(category, fl, q, a):
    if category == "catering":
        if fl == "cafeteria":
            print(cafeteria.cafeteria_questions)
            cafeteria.add(q, a)
            print(cafeteria.cafeteria_questions)
    if category == "dorms":
        if fl == "dorms":
            print(dorms.dorms.dorm_questions)
            dorms.dorms.add(q, a)
            print(dorms.dorms.dorm_questions)

    if category == "internet":
        if fl == "internet":
            print(internet.internet.dorm_questions)
            internet.internet.add(q,a)
            print(internet.internet.dorm_questions)
    
    if category == "teleportation":
        if fl == "rings":
            print(teleportation.rings.ring_questions)
            teleportation.rings.add(q,a)
            print(internet.internet.dorm_questions)
    
    if category == "departments":
        if fl == "ceng":
            print(departments.ceng.ceng_questions)
            departments.ceng.add(q,a)
            print(departments.ceng.ceng_questions)

def answer_question(category, fl, q):
    if category == "catering":
        if fl == "cafeteria":
            cafeteria.answer(q)

def admin_listener():
    #TODO: ADMINDEN KOMUT BEKLE
    ...

add_question("catering","cafeteria","Bugün yemekhanede ne yemek var", 1) #If the answer is a number, then we fetch the answer by calling fetch.
answer_question("catering","cafeteria","Bugün yemekhanede ne yemek var")