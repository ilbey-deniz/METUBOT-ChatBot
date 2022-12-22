
import fasttext
import fasttext.util
import json
import nltk
from nltk.tokenize import RegexpTokenizer
from snowballstemmer import TurkishStemmer
import numpy as np
from numpy.linalg import norm
from pathlib import Path
# fasttext.util.download_model('tr', if_exists='ignore')


cos_sim = lambda q_vector, vector : np.dot(q_vector, vector)/(norm(q_vector)*norm(vector))


STOPWORD_LIST = nltk.corpus.stopwords.words('turkish')
CUSTOMWORD_LIST = ["wifi", "section", "metu", "office"] # custom word list

f = Path(__file__).with_name('answers.json').open()
ANSWERS = json.load(f)

f = Path(__file__).with_name('question_categories.json').open()
QUESTIONS = json.load(f)

QUESTION_VECTORS= {}

# preprocessor for question strings to transform strings to word arrays.
# TODO: a better alternative than snowball stemmer should be used.
def preProcessor(sentence):
    sentence = sentence.lower()
    tokenizer = RegexpTokenizer(r'\w+') # removes all punctuation
    words = tokenizer.tokenize(sentence)

    ts = TurkishStemmer()
    result = []
    for word in words:
        if word not in STOPWORD_LIST:
            if word in CUSTOMWORD_LIST:
                result.append(word)
            else:
                result.append(ts.stemWord(word))
    return result



# Gets the questions dictionary and returns dictionary of dictionaries
# where subdictionaries consists of keys as each term and values as
# number of occurencies.
# This version treats all questions in a category as a whole document.
def TF(questions):
    result = {}
    for category in questions:
        result[category] = {}
        for question in questions[category]:
            term_arr = preProcessor(question)
            for term in term_arr:
                if term not in result[category]:
                    result[category][term] = 1
                else:
                    result[category][term] += 1
    return result

def normalizedTF(questions):
    result = {}
    tf = TF(questions)
    for category in tf:
        result[category] = {}
        no_of_terms = len(tf[category])
        for term in tf[category]:
            result[category][term] = tf[category][term] / no_of_terms
    return result

# Calculates inverse document frequency of a term
def IDF(term, questions):
    number_of_documents = len(questions)
    number_of_occurences = 0
    tf = TF(questions)
    for category in tf:
        # number_of_documents += len(tf) # counting all questions, not categories; this can be changed
        if term in tf[category]:
            number_of_occurences+=1
    if number_of_occurences == 0:
        return 0
    return 1 + np.log(number_of_documents / number_of_occurences)


def TFxIDF(terms_string, questions):
    result = {}
    normal_tf = normalizedTF(questions)
    terms = preProcessor(terms_string)

    for category in normal_tf:
        result[category] = {}
        for term in terms:
            idf = IDF(term, questions)
            if term in normal_tf[category]:
                result[category][term] = normal_tf[category][term] * idf
            else:
                result[category][term] = 0
    return result

# returns the most likely category as an heuristic for fasttext classifier
def categoryHeuristic(query, questions):
    tfidf = TFxIDF(query, questions)
    max_val = -1
    max_category = ""
    for category in tfidf:
        for term in tfidf[category]:
            if tfidf[category][term] > max_val:
                max_category = category
                max_val = tfidf[category][term]
    return max_category



def getQuestionVectors(ft, raw_questions):
    question_vectors = {}
    for key in raw_questions:
        question_vectors[key] = []
        for q in raw_questions[key]:
            question_vectors[key].append(ft.get_sentence_vector(q))
    return question_vectors


def questionClassifier(ft, user_question, question_vectors, raw_questions):
    q_vector = ft.get_sentence_vector(user_question)

    most_similar_question = ""
    most_similar_category = ""

    max_similarity = 0

    tfidf_category = categoryHeuristic(user_question, raw_questions)

    for key in question_vectors:
        for vector, question in zip(question_vectors[key], raw_questions[key]):
            sim = cos_sim(q_vector, vector)
            if sim > max_similarity:
                max_similarity = sim
                most_similar_question = question
                most_similar_category = key

    if most_similar_category != tfidf_category:
        print("--MUHTEMEL YANLIS ANLAMALAR SOZ KONUSU--")
        print("TF.IDF kategori tahmini: %s" % tfidf_category)
        print("FastText kategori tahmini: %s" % most_similar_category)
        # search for the question under the tfidf heuristic category
        most_similar_question = ""
        most_similar_category = ""

        max_similarity = 0

        most_similar_category = tfidf_category
        for vector, question in zip(question_vectors[tfidf_category], raw_questions[tfidf_category]):
            sim = cos_sim(q_vector, vector)
            if sim > max_similarity:
                max_similarity = sim
                most_similar_question = question

    else:
        print("Soru kategorisi: %s" % most_similar_category)
        print("En yakin soru: %s" % most_similar_question)

    return (most_similar_category, most_similar_question)


def getAnswer(ft, user_question):
    global QUESTION_VECTORS

    if QUESTION_VECTORS=={}:
        QUESTION_VECTORS = getQuestionVectors(ft, QUESTIONS)
    category,question = questionClassifier(ft, user_question, question_vectors=QUESTION_VECTORS, raw_questions=QUESTIONS)
    ans = ANSWERS[category]
    return ans

