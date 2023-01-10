from bs4 import BeautifulSoup
import time 
import requests

months = ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]
weekdays = ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"]

def initialize(url):
    page = requests.get(url)
    #page'in class'ı <class 'requests.models.Response'> ve stringe çevirirsek html dosyası gibi oluyor.
    soup = BeautifulSoup(page.content, "html.parser")
    #soup sayesinde page'i parse ediyoruz.
    return soup


def saat():
    now = time.localtime()
    md = str(now.tm_mday)
    wd = weekdays[now.tm_wday]
    mon = months[now.tm_mon-1]
    y = str(now.tm_year)
    h = "0" + str(now.tm_hour) if now.tm_hour<10 else str(now.tm_hour)
    m = "0" + str(now.tm_min) if now.tm_min<10 else str(now.tm_min)
    s = "0" + str(now.tm_sec) if now.tm_sec<10 else str(now.tm_sec)
    return "Bugünün tarihi: " + md + " " + mon + " " + y + ", " + wd + " " + h + ":" + m + ":" + s + "."


def takvim():
    d = time.localtime()
    url = ""
    if d.tm_mon < 10:
        url = "http://oidb.metu.edu.tr/tr/odtu-ankara-ve-erdemli-kampuslari-" + str(d.tm_year-1) +  "-"  + str(d.tm_year) + "-akademik-takvim"
    else:
        url = "http://oidb.metu.edu.tr/tr/odtu-ankara-ve-erdemli-kampuslari-" + str(d.tm_year) +  "-"  + str(d.tm_year+1) + "-akademik-takvim"
    
    return "Akademik takvim için " + url + " inceleyebilirsiniz."