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

def cengcurriculum():
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

def ring_saatleri():
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


def saatler():
    soup = initialize("https://kafeterya.metu.edu.tr/yemek-saatleri")
    a = soup.find(class_="field-items")
    return a.text.strip()


def takvim():
    d = time.localtime()
    url = ""
    if d.tm_mon < 10:
        url = "http://oidb.metu.edu.tr/tr/odtu-ankara-ve-erdemli-kampuslari-" + str(d.tm_year-1) +  "-"  + str(d.tm_year) + "-akademik-takvim"
    else:
        url = "http://oidb.metu.edu.tr/tr/odtu-ankara-ve-erdemli-kampuslari-" + str(d.tm_year) +  "-"  + str(d.tm_year+1) + "-akademik-takvim"
    
    return "Akademik takvim için " + url + " inceleyebilirsiniz."



