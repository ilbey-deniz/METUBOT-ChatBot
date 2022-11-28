from flask import Blueprint, Response, request
import json
# from bson import json_util
from nlp.fasttext.fast_text import match_questions
from backend.database.mysql import questions

fast_text = Blueprint("fast_text", __name__)

path = "./input/"

@fast_text.route(
    "/example/sentence/",
    endpoint="match question and write DB")
def get_result_sentence():
    sentence = request.args.get("sentence")
    # dummy_response = sentence + " ile neyi kasteddiğinizi anlayamadım."
    dummy_response, similarity = match_questions(sentence)
    similarity = float(similarity)

    if similarity < 0.70:
        questions.create_question_db()
        questions.create_table()
        questions.insert_question(sentence, dummy_response, similarity)

    dummy_response = json.dumps(dummy_response, indent=4, ensure_ascii=False)
    response = Response(dummy_response, mimetype="application/json", status=200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@fast_text.route(
    "/sample/",
    endpoint="get similarity")
def get_sentence_with_similarity():
    print("sa")
    sentence = request.args.get("sentence")
    # dummy_response = sentence + " ile neyi kasteddiğinizi anlayamadım."
    dummy_response, similarity = match_questions(sentence)
    similarity = float(similarity)
    # dummy_response = json.dumps(dummy_response, indent=4)
    print(similarity)
    result = {}
    result["sentence"] = sentence
    result["matched_sentence"] = dummy_response
    result["similarity"] = similarity
    print(result)

    result = json.dumps(result, indent=4, ensure_ascii=False)

    response = Response(result, mimetype="application/json", status=200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
