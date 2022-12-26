import requests
from bs4 import BeautifulSoup



def ring_saatleri(): #qi = question index
    def initialize(url):
        page = requests.get(url)
        #page'in class'ı <class 'requests.models.Response'> ve stringe çevirirsek html dosyası gibi oluyor.
        soup = BeautifulSoup(page.content, "html.parser")
        #soup sayesinde page'i parse ediyoruz.
        return soup
    soup = initialize("https://tim.metu.edu.tr/ring-services")
    a = soup.find(class_="menu-block-wrapper menu-block-ctools-main-menu-1 menu-name-main-menu parent-mlid-0 menu-level-2")
    b = a.find_all(class_="leaf")
    d = ""
    for c in b[:-3]:
        d += c.text.strip() + "\n"
    d += b[-3].text.strip()
    return d