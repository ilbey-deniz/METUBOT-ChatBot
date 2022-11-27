import fasttext
import fasttext.util
# from fastText.python.fasttext_module.fasttext.util import util
fasttext.util.download_model('tr', if_exists='ignore')

from numpy import dot
from numpy.linalg import norm
from scipy import spatial

def spatialDistance(vector1, vector2):
    return spatial.distance.euclidean(vector1, vector2)

ft = fasttext.load_model(r'cc.tr.300.bin')

questions = {
    "sifre":[
        "öğrenci şifremi unuttum, nasıl yenileyebilirim?",
        "ODTU kullanıcı şifremi hatırlamıyorum, ne yapmam lazım?",
        "metu mail şifremi kaybettim, nasıl sıfırlarım?",
        "parolamı unuttum",
        "metumail şifrem neydi"
        ],
    "lisanslı yazılımlar": [
        "Microsoft Office'i öğrenci mailimle nasıl kullanabilirim?",
        "ücretsiz Autocad kullanmak için ne yapmam lazım",
        "exceli metu mailimle nasıl kullanabilirim?"
        ],
    "wifi":[
        "meturoam a nasıl bağlanabilirim",
        "odtu wifi nasıl bağlanırım",
        "hangi wifi a bağlanmam gerek",
        "eduroam şifresi neydi"
    ]
}

question_vectors = {}
for key in questions:
    question_vectors[key] = []
    for q in questions[key]:
        question_vectors[key].append(ft.get_sentence_vector(q))

def match_questions(user_question):
    # user_question = input("Nasıl yardımcı olabilirim?")
    q_vector = ft.get_sentence_vector(user_question)

    most_similar_question = ""
    most_similar_category = ""

    max_similarity = 0
    category_max_similarity = 0

    for key in question_vectors:
        for vector, question in zip(question_vectors[key], questions[key]):
            sim = dot(q_vector, vector) / (norm(q_vector) * norm(vector))
            if sim > max_similarity:
                max_similarity = sim
                most_similar_question = question
                most_similar_category = key

    print("Soru kategorisi: %s" % most_similar_category)
    print("En yakın soru: %s" % most_similar_question)
    return str(most_similar_question), max_similarity
