import requests
from bs4 import BeautifulSoup

def initialize(url):
    page = requests.get(url)
    #page'in class'ı <class 'requests.models.Response'> ve stringe çevirirsek html dosyası gibi oluyor.
    soup = BeautifulSoup(page.content, "html.parser")
    #soup sayesinde page'i parse ediyoruz.
    return soup

def yemek():
    soup= initialize("https://kafeterya.metu.edu.tr/")
    a = soup.find(class_="view-content")
    b = a.find_all(class_ = "rdf-meta element-hidden")
    vej = a.find_all(class_ = "vejeteryan")
    prompt = "Bugün yemekhanede "+ str(b[0].get("content")) + ", " + str(b[1].get("content")) + ", " + str(b[2].get("content")) + " ve " + str(b[3].get("content")) +  " var.\n"
    prompt += vej[0].text.strip()
    return prompt

def saatler():
    soup = initialize("https://kafeterya.metu.edu.tr/yemek-saatleri")
    a = soup.find(class_="field-items")
    return a.text.strip()