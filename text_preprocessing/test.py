import re

from nltk.corpus import stopwords

import zeyrek

from zemberek import (
    TurkishSentenceNormalizer,
    TurkishMorphology,
)

def text_preprocess(text):
    morphology = TurkishMorphology.create_with_defaults()
    normalizer = TurkishSentenceNormalizer(morphology)
    text = normalizer.normalize(text)  # normalize the text
    text = text.lower()  # lower case
    text = re.sub('[0-9]+', '', text)
    text = re.sub(r'[^\w\s]', '', text)  # remove punctuation emotes and numbers

    analyzer = zeyrek.MorphAnalyzer()


    stops = set(stopwords.words('turkish'))
    word_list = text.split(" ")
    word_list = [w for w in word_list if w not in stops and w != '']  # stop word elimination

    lem_list = []
    for word in word_list:
        lem_word = analyzer.lemmatize(word)
        lem_list.append(lem_word)

    return lem_list

text = "bizim ülkede buna kafası çalışan çıkmaz ama senaryoda polat'ı artık kahraman gibi değil de " \
       "(hem yaşı hem de hikayedeki yeri gereği) baronlaşmış olarak gösterip, genç bir oyuncuyla onu " \
       "devirmek üstüne hikaye yazılabilir. sonuçta güç yozlaştırır, birçok vatansever kontrgerilla yeterince " \
       "güç elde edindikten sonra mafyalaştı bu ülkede. en azından tutarlı iş yapılmış olur."

text2 = "Sıkı Bir Müzik Dinleyicisinden: Pentagram'ın Yeni Albümü Makina Elektrika'nın İncelemesi " \
        "Türk metal grubu Pentagram'ın 9 Eylül 2022'de yayınladıkları 8. stüdyo albümü, uzun süren bekleyişin ardından" \
        " platformlardaki yerini aldı. Şarkı şarkı inceliyoruz."

text3 = "Seni izleyip oynua giriyorum destem mezarlık destesi 2x e geliyoruz adam arkadan elektro dev" \
        " atıyor ben defans kuruyum fln diyorum senin gibi daha sobra elektro devin önüne mega şovalye yada" \
        " elitbarbarlar atıyolar benim arenamda taktik falan yapılmıyor oyundan soğdum toxic kartlar yuzuden ama sen saol oyunu öğretiyorsun"

text4 = "Güne umutla başladık. Şiddet sonucu engelli kalan Fatma Arpak’ın 500 bin ₺ sinin 240 bin ₺ sini" \
        " sizler toplamıştınız. Kalan 260 bin ₺ yi @KriptoEfsanesi kardeşimiz karışladı.👏👏👏 Sayenizde " \
        "yüzlerce insan hayata döndü. Sizlere nasıl teşekkür edeceğim bilmiyorum 🙏"


print(text_preprocess(text))
print("*------------------------*")
print(text_preprocess(text2))
print("*------------------------*")
print(text_preprocess(text3))
print("*------------------------*")
print(text_preprocess(text4))

