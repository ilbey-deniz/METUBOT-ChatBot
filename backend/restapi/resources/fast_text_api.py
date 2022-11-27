from flask import Blueprint, Response, request
import json
# from bson import json_util
from nlp.fasttext.fast_text import match_questions
from backend.database.mysql import questions

fast_text = Blueprint("fast_text", __name__)

path = "./input/"


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
