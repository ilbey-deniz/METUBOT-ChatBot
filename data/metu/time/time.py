from bs4 import BeautifulSoup
from datetime import datetime
import requests

aylar = ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]

def initialize(url):
    page = requests.get(url)
    #page'in class'ı <class 'requests.models.Response'> ve stringe çevirirsek html dosyası gibi oluyor.
    soup = BeautifulSoup(page.content, "html.parser")
    #soup sayesinde page'i parse ediyoruz.
    return soup


def saat():
    now = datetime.now()
    d = now.date()
    h = now.hour
    min = now.minute
    sec = now.second
    if h<10:
        h = "0" + str(h)
    if min<10:
        min = "0" + str(min)
    if sec<10:
        sec = "0" + str(sec)
    tarih = "Bugünün tarihi: " + str(d.day+1) + " " + aylar[d.month-1] + " " + str(d.year) + ", " + str(h) + ":" + str(min) + ":" + str(sec) + "."
    return tarih


def takvim():
    d = datetime.now().date()
    url = ""
    if d.month < 10:
        url = "http://oidb.metu.edu.tr/tr/odtu-ankara-ve-erdemli-kampuslari-" + str(d.year-1) +  "-"  + str(d.year) + "-akademik-takvim"
    else:
        url = "http://oidb.metu.edu.tr/tr/odtu-ankara-ve-erdemli-kampuslari-" + str(d.year) +  "-"  + str(d.year+1) + "-akademik-takvim"
    
    return "Akademik takvim için " + url + " inceleyebilirsiniz."