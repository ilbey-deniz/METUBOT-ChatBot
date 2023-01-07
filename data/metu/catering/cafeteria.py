import requests
from bs4 import BeautifulSoup

def initialize(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def yemek():
    try:
        soup= initialize("https://kafeterya.metu.edu.tr/")
        b = soup.find_all(class_ = "rdf-meta element-hidden")
        vej = soup.find_all(class_ = "vejeteryan")
        prompt = "Öğle yemeği:\n\t"+ str(b[0].get("content")) + ", " + str(b[1].get("content")) + ", " + str(b[2].get("content")) + " ve " + str(b[3].get("content")) +  "\n"
        prompt += "\t" + vej[0].text.strip() + "\n"
        prompt += "Akşam yemeği:\n\t"+ str(b[4].get("content")) + ", " + str(b[5].get("content")) + ", " + str(b[6].get("content")) + " ve " + str(b[7].get("content")) +  "\n"
        prompt += "\t" + vej[1].text.strip()
    except:
        prompt = "BUgün yemekhanede yemek çıkmıyor."

    return prompt

def saatler():
    soup = initialize("https://kafeterya.metu.edu.tr/yemek-saatleri")
    a = soup.find(class_="field-items")
    return a.text.strip()

def fiyat(role="Öğrenci"):
    d = {
        "Personel: Ek Göstergesiz (Ek:0)":1,
        "Personel: Ek Göstergeli (0 üzeri ve 2200 dahil)":2,
        "Personel: Ek Göstergeli (2200 üzeri ve 3000 dahil)":3,
        "Personel: Ek Göstergeli (3600 dahil ve üzeri)":4,
        "Personel: Sözleşmeli":5,
        "Personel: İşçi":6,
        "Öğrenci":7,
        "Misafir":8,
        "Diğer":9
    }

    diff = d[role]


    soup = initialize("http://kafeterya.metu.edu.tr/tabldot-yemek-fiyatlari")
    a = soup.find(property= "content:encoded")
    prompt = a.p.strong.text.strip() + "\n"
    b = a.find(class_ ="table")
    c= list(filter(lambda x: x != "", b.text.strip().split("\n")))
    prompt += role + "\n"
    prompt += c[0] + ": " + c[4*diff] + "\n"
    prompt += c[1] + ": " + c[4*diff+1] + "\n"
    prompt += c[2] + ": " + c[4*diff+2]
    return prompt

print(yemek())