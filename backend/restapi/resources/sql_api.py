from flask import Blueprint, Response, request
import json
from backend.database.mysql.questions import *


mysql = Blueprint("mysql", __name__)

# path = "./input/"

@mysql.route(
    "/addQuestion",
    endpoint="add question to db")
def add_one_question():
    question = request.args.get("question")
    answer = request.args.get("answer")
    category = request.args.get("category")

    # similarity = float(similarity)
    add_question(question, answer, category)

    response_message = "question is added"
    response_message = json.dumps(response_message, indent=4, ensure_ascii=False)
    response = Response(response_message, mimetype="application/json", status=200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@mysql.route(
    "/getQuestions",
    endpoint="get all questions")
def get_all_questions():
    query_res = get_all_questions()
    result = dict()
    result["data"] = query_res

    result = json.dumps(result, indent=4, ensure_ascii=False)
    response = Response(result, mimetype="application/json", status=200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
