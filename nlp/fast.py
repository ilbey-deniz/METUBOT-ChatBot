import fasttext
import fasttext.util
import json
import nltk
from nltk.tokenize import RegexpTokenizer
from snowballstemmer import TurkishStemmer
import numpy as np
from numpy.linalg import norm
from pathlib import Path
import random
#from gensim.models import KeyedVectors
from sentence_transformers import SentenceTransformer

#fasttext.util.download_model('tr', if_exists='ignore')

MODEL_DIR = r"./cc.tr.300.bin"
ft = None
word_vectors = None
cos_sim = lambda q_vector, vector : np.dot(q_vector, vector)/(norm(q_vector)*norm(vector))


#STOPWORD_LIST = nltk.corpus.stopwords.words('turkish')
CUSTOMWORD_LIST = ["wifi", "section", "metu", "office"] # custom word list


QUESTION_VECTORS = {}

f = Path(__file__).with_name('qa_pairs.json').open()
QA = json.load(f)["qa-pairs"]

THRESHOLD = 0.4
DEFAULT_ANSWER = "Üzgünüm, ne sormak istediğinizi anlayamadım. sorunuzu bildirmek ister misiniz?"

# preprocessor for question strings to transform strings to word arrays.
def preProcessor(sentence):
    sentence = sentence.lower()
    return sentence



# adds a new field 'q_vectors' 
# that stores sentence vectors of each question.
# IMPORTANT: assign the result to QA constant array  
def NEWgetQuestionVectors(questions_answers):
    global ft

    for qa_pair in questions_answers:
        if "q_vectors" not in qa_pair:
            qa_pair["q_vectors"] = []
        for q in range(len(qa_pair["question"])):
            qa_pair["q_vectors"].append(ft.get_sentence_vector(qa_pair["question"][q]))
    return questions_answers  


def NEWquestionClassifier(user_question, questions_answers):
    global ft

    q_vector = ft.get_sentence_vector(user_question)

    most_similar_question = ""
    most_similar_category = ""
    most_similar_indice = 0

    max_similarity = 0

    for qa in questions_answers:
        for q in range(len(qa["q_vectors"])):
            sim = cos_sim(q_vector, qa["q_vectors"][q])
            if sim > max_similarity:
                max_similarity = sim
                most_similar_question = qa["question"][q]
                most_similar_category = qa["category"]
                most_similar_indice = questions_answers.index(qa)
    
    print("Benzerlik skoru: " + str(max_similarity))
    print("Soru kategorisi: %s" % most_similar_category).encode()
    print("En yakin soru: %s" % most_similar_question).encode()

    if max_similarity < THRESHOLD:
        return None
    return most_similar_indice


def NEWgetAnswer(user_question):
    global ft
    global QA

    QA = NEWgetQuestionVectors(QA)
    q_index = NEWquestionClassifier(user_question, questions_answers=QA)
    if not q_index:
        return DEFAULT_ANSWER
    ans = random.choice(QA[q_index]["answer"])
    return ans

def init():
    #global ft

    #ft = fasttext.load_model(MODEL_DIR)

    global word_vectors
    word_vectors = SentenceTransformer('emrecan/bert-base-turkish-cased-mean-nli-stsb-tr')

    #word_vectors = KeyedVectors.load_word2vec_format('trmodel', binary=True)

def vectorize(question):
    global word_vectors
    
    return word_vectors.encode(question).tolist()
    return ft.get_sentence_vector(question)