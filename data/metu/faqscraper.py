import requests 
from bs4 import BeautifulSoup
import json 

#kodumu türkçe anlatıyorum arkadaşlar hazır mıyız?
#request ve soup'a ihtiyaç var
#sonra soruları çekip dictionarye atıp yazdıracağız

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
        subcategory_dict["questions"] = []
        subcategory_dict["answers"] = []
        subcategories.append({i:subcategory_dict})
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
        categories.append({i:category_dict})
    return categories #is a list of dictionaries
    

def fill_cate_dict(soup):
    l = get_categories(soup)
    return {"categories": l, "category_count": len(l)}

def write_json(dict,jsonfilepath):
    json_string = json.dumps(dict)
    f = open(jsonfilepath, "a")
    f.write(json_string)
    f.close()
    return



#MAIN BURADAN BAŞLIYOR
json_path = "./faq_categories.json"

URL = "https://faq.cc.metu.edu.tr/tr"
soup = initialize(URL)

cate_dict = fill_cate_dict(soup) 
write_json(cate_dict,json_path)
print(cate_dict)