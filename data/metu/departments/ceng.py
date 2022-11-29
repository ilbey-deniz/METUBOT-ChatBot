import requests
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
        return fetch(ceng_questions[question])

def turkify(prompt):
    prompt = prompt.replace("\\" + "xc3" + "\\" + "x87","Ç")
    prompt = prompt.replace("\\" + "xc4" + "\\" + "x9e","Ğ")
    prompt = prompt.replace("\\" + "xc4" + "\\" + "xb0","İ")
    prompt = prompt.replace("\\" + "xc3" + "\\" + "x96","Ö")
    prompt = prompt.replace("\\" + "xc5" + "\\" + "x9e","Ş")
    prompt = prompt.replace("\\" + "xc3" + "\\" + "x9c","Ü")
    return prompt

def fetch(qi): #qi = question index
    if qi==1: #zorunlu
        r = requests.get("https://ceng.metu.edu.tr/undergraduate-curriculum")
        c = str(r.content)
        ckey = "course_code"
        dkey = "course"
        key = '<span property="dc:title" content="'
        dersler = []
        i = 1
        while i!=-1:
            i = c.find(ckey,i)
            ilk = c.find(">",i)
            son = c.find("<",ilk)
            code = c[ilk+1:son]

            if code=="CENG492":
                i=-1
            else:
                i=son
            i2 = c.find(dkey,son)
            ilk2 = c.find(">",i2)
            son2 = c.find("<",ilk2)
            ders = c[ilk2+1:son2]
            dersler.append([code,ders])
        prompt = "CENG'in zorunlu dersleri:\n\n"
        for ders in dersler:
            if(not ders[0]):
                continue
            if(ders[1]):
                prompt += ders[0] + " - " + ders[1] + "\n"
            else:
                prompt += ders[0] + "/"
        return prompt[:-1]

    
