import requests 
from bs4 import BeautifulSoup
import json 

#kodumu türkçe anlatıyorum arkadaşlar hazır mıyız?
#request ve soup'a ihtiyaç var
#sonra soruları çekip dictionarye atıp yazdıracağız
questions = []
answers = []
URL = "https://faq.cc.metu.edu.tr/tr"


def initialize(url):
    page = requests.get(url)
    #page'in class'ı <class 'requests.models.Response'> ve stringe çevirirsek html dosyası gibi oluyor.
    soup = BeautifulSoup(page.content, "html.parser")
    #soup sayesinde page'i parse ediyoruz.
    return soup

def get_subcategories(category):
    subcategories = []
    a = category.find_all(class_="menu__item")
    # a is the div of categories
    for i in range(len(a)):
        b = a[i].find_all(class_="menu__link")
        c = b[0].text.strip() 
        #c is the name of the subcategory
        subcategory_dict = {}
        subcategory_dict["name"] = c
        subcategory_dict["questions"] = get_questions(b[0])
        subcategory_dict["answers"] = get_answer(b[0])
        subcategories.append(subcategory_dict)
    return subcategories

def get_categories(soup):
    categories = []
    a = soup.find(class_="nice-menu nice-menu-down nice-menu-main-menu")
    b = a.find_all(class_="menuparent")
    #b is the div of categories
    for i in range(len(b)): #for each category
        c = b[i].find_all(class_="menu__link")
        d= c[0].text.strip()
        #d is the name of the category

        category_dict = {}
        category_dict["name"] = d
        s_list = get_subcategories(b[i])
        category_dict["subcategories"] = s_list
        category_dict["subcategory_count"] = len(s_list)
        categories.append(category_dict)
    return categories #is a list of dictionaries
    
def get_questions(para):
    sub_url = "https://faq.cc.metu.edu.tr/tr/groups/ip-ve-mac"
    sub_url = URL + para.get("href")
    print(sub_url)
    sub_soup = initialize(sub_url)
    a = sub_soup.find(class_="view-content")
    b = a.find_all(href=True)
    for quest in b:
        url_quest = quest.get("href")
        q = quest.text.strip()
        questions.append(q) 
        #answers.append(get_answer(url_quest))
    return []
def get_answer(b):
    return "answer"

def fill_cate_dict(soup):
    l = get_categories(soup)
    return {"categories": l, "category_count": len(l)}

def write_json(dict,jsonfilepath):
    json_string = json.dumps(dict)
    f = open(jsonfilepath, "w")
    f.write(json_string)
    f.close()
    return



#MAIN BURADAN BAŞLIYOR
cate_json_path = "./faq_categories.json"
question_json_path = "./faq_questions.json"
answer_json_path = "./faq_answers.json"




soup = initialize(URL)

cate_dict = fill_cate_dict(soup) 
write_json(cate_dict,cate_json_path)

""" question_dict = fill_question_dict(soup)
write_json(question_dict,question_json_path)

answer_dict = fill_answer_dict(soup)
write_json(answer_dict,answer_json_path) """