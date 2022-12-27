import requests
from bs4 import BeautifulSoup

def initialize(url):
    page = requests.get(url)
    #page'in class'ı <class 'requests.models.Response'> ve stringe çevirirsek html dosyası gibi oluyor.
    soup = BeautifulSoup(page.content, "html.parser")
    #soup sayesinde page'i parse ediyoruz.
    return soup

def turkify(prompt):
    prompt = prompt.replace("\\" + "xc3" + "\\" + "x87","Ç")
    prompt = prompt.replace("\\" + "xc4" + "\\" + "x9e","Ğ")
    prompt = prompt.replace("\\" + "xc4" + "\\" + "xb0","İ")
    prompt = prompt.replace("\\" + "xc3" + "\\" + "x96","Ö")
    prompt = prompt.replace("\\" + "xc5" + "\\" + "x9e","Ş")
    prompt = prompt.replace("\\" + "xc3" + "\\" + "x9c","Ü")
    return prompt

""" def yemek(): #bugün yemekhanede ne var
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
    return prompt """

def yemek():
    soup= initialize("https://kafeterya.metu.edu.tr/")
    a = soup.find(class_="view-content")
    b = a.find_all(class_ = "rdf-meta element-hidden")
    vej = a.find_all(class_ = "vejeteryan")
    prompt = "Bugün yemekhanede "+ str(b[0].get("content")) + ", " + str(b[1].get("content")) + ", " + str(b[2].get("content")) + " ve " + str(b[3].get("content")) +  " var.\n"
    prompt += vej[0].text.strip()
    return prompt