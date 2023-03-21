from flask import Flask, jsonify, request, Response
from ElasticAnswerer import ElasticAnswerer
from FasttextAnswerer import FasttextAnswerer
from AnswerGeneratorMetu import AnswerGeneratorMetu
from data.metu.json_qapairs_manager import add_questions_manually
from backend.database.mysql.questions import *

app = Flask(__name__)

answer_generator = AnswerGeneratorMetu()
elastic_answerer = ElasticAnswerer(answer_generator)
fasttext_answerer = FasttextAnswerer(answer_generator)

@app.route('/ask')
def get_incomes():
    return elastic_answerer.generatedAnswer(request.args.get('question'))

@app.route('/askFast')
def get_incomes_fast():
    return fasttext_answerer.generatedAnswer(request.args.get('question'))

@app.route('/addQuestion')
def add_one_questions():
    category = request.args.get("category")
    question = request.args.get("question")
    answer = request.args.get("answer")
    print(category, question, answer)
    add_question(question, answer, category)

    response_message = "question is added"
    response_message = json.dumps(response_message, indent=4, ensure_ascii=False)
    response = Response(response_message, mimetype="application/json", status=200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getAllQuestions')
def get_all_questions():
    query_res = query_all_questions()
    result = dict()
    result["data"] = query_res

    result = json.dumps(result, indent=4, ensure_ascii=False)
    response = Response(result, mimetype="application/json", status=200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/reportQuestion')
def report_questions():
    question_id = request.args.get("question_id")
    similarity = request.args.get("similarity")
    asked_question = request.args.get("asked_question")
    report_message = request.args.get("report_message")
    is_liked = request.args.get("is_liked")
    add_feedback(int(question_id), float(similarity), asked_question, bool(is_liked), report_message)

    response_message = "feedback is added"
    response_message = json.dumps(response_message, indent=4, ensure_ascii=False)
    response = Response(response_message, mimetype="application/json", status=200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAllReports')
def get_all_report():
    query_feedback = query_all_feedbacks()
    result = dict()
    result["data"] = query_feedback

    result = json.dumps(result, indent=4, ensure_ascii=False)
    response = Response(result, mimetype="application/json", status=200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    print("NLP Backend api started. Ask your question with get request to /ask?question=your_question")
    app.run(host="0.0.0.0", port="8080", debug=False)