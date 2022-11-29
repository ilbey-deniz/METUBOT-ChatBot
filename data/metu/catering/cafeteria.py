import requests
cafeteria_questions = {}



def add(question, answer):
    cafeteria_questions[question] = answer
def remove(question):
    cafeteria_questions.pop(question)
def replace(question, newanswer):
    cafeteria_questions[question] = newanswer

def answer(question):
    if type(cafeteria_questions[question]) != int:
        return cafeteria_questions[question]
    else:
        fetch(cafeteria_questions[question])

def turkify(prompt):
    prompt = prompt.replace("\\" + "xc3" + "\\" + "x87","Ç")
    prompt = prompt.replace("\\" + "xc4" + "\\" + "x9e","Ğ")
    prompt = prompt.replace("\\" + "xc4" + "\\" + "xb0","İ")
    prompt = prompt.replace("\\" + "xc3" + "\\" + "x96","Ö")
    prompt = prompt.replace("\\" + "xc5" + "\\" + "x9e","Ş")
    prompt = prompt.replace("\\" + "xc3" + "\\" + "x9c","Ü")
    return prompt

def fetch(qi): #qi = question index
    if(qi == 1): #yemekhanedeki yemekler
        r = requests.get("https://kafeterya.metu.edu.tr/")
        key = '<span property="dc:title" content="'
        c = str(r.content)
        i1 = c.find(key)
        s1 = c.find('"',i1+len(key))
        i2 = c.find(key,i1+len(key))
        s2 = c.find('"',i2+len(key))
        i3 = c.find(key,i2+len(key))
        s3 = c.find('"',i3+len(key))
        i4 = c.find(key,i3+len(key))
        s4 = c.find('"',i4+len(key))
        yemek1 = c[i1+len(key):s1]
        yemek2 = c[i2+len(key):s2] 
        yemek3 = c[i3+len(key):s3]
        yemek4 = c[i4+len(key):s4]
        prompt = "Bugün yemekhanede "+ yemek1 + ", " + yemek2 + ", " + yemek3 + " ve " + yemek4 +  " var."
        prompt = turkify(prompt)
        print(prompt)
