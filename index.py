from flask import Flask, jsonify, request, Response, render_template
import json
from flask_socketio import SocketIO, send, emit
from threading import Timer
from ElasticAnswerer import ElasticAnswerer
from FasttextAnswerer import FasttextAnswerer
from DummyAnswerer import DummyAnswerer
from Answerer import Answerer
from AnswerGeneratorMetu import AnswerGeneratorMetu
from data.metu.json_qapairs_manager import add_questions_manually
from backend.database.mysql.questions import *


answer_generator = AnswerGeneratorMetu()

#answerer: Answerer = FasttextAnswerer(answer_generator)
answerer: Answerer = ElasticAnswerer(answer_generator)
#answerer: Answerer = DummyAnswerer(answer_generator)

app = Flask(__name__,
            static_folder = "./frontend/dist/static",
            template_folder = "./frontend/dist")

app.config['SECRET_KEY'] = '\xc9\xf6yGRi{k%9>\x0bQI\xe6)\x0f\xaf\xc0\x05\x8b\xc7\x87\x8c'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/addQuestion')
def add_one_questions():
    print('ADDING QUESTİON')
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

@app.route('/deleteQuestion')
def delete_one_questions():
    print('QUESTION IS DELETING')
    question_id = request.args.get("question_id")
    delete_question_with_id(int(question_id))

    response_message = "question is deleted"
    response_message = json.dumps(response_message, indent=4, ensure_ascii=False)
    response = Response(response_message, mimetype="application/json", status=200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/updateQuestion')
def update_one_questions():
    print('QUESTION IS UPDATING')
    question_id = request.args.get("question_id")
    new_category = request.args.get("new_category")
    new_question = request.args.get("new_question")
    new_answer = request.args.get("new_answer")
    print(new_category, new_question, new_answer)
    update_question(int(question_id), new_question, new_answer, new_category)

    response_message = "question is updated"
    response_message = json.dumps(response_message, indent=4, ensure_ascii=False)
    response = Response(response_message, mimetype="application/json", status=200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getFrequentQuestions')
def get_frequent_questions():
    number_of_data = request.args.get("number_of_data")
    query_res = get_most_frequent_questions(int(number_of_data))

    result = dict()
    result["data"] = query_res

    result = json.dumps(result, indent=4, ensure_ascii=False)
    response = Response(result, mimetype="application/json", status=200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getLikedQuestions')
def get_liked_questions():
    number_of_data = request.args.get("number_of_data")
    query_res = get_most_liked_questions(int(number_of_data))

    result = dict()
    result["data"] = query_res

    result = json.dumps(result, indent=4, ensure_ascii=False)
    response = Response(result, mimetype="application/json", status=200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAverageSimilarity')
def get_avg_similarity():
    query_res = get_average_similarity()
    result = dict()
    result["data"] = query_res

    result = json.dumps(result, indent=4, ensure_ascii=False)
    response = Response(result, mimetype="application/json", status=200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getFeedbacks')
def query_feedbacks():
    is_liked = request.args.get("is_liked")
    min_similarity = request.args.get("min_similarity")
    max_similarity = request.args.get("max_similarity")

    query_feedback = advance_query_feedbacks(bool(is_liked), float(min_similarity), float(max_similarity))
    result = dict()
    result["data"] = query_feedback

    result = json.dumps(result, indent=4, ensure_ascii=False)
    response = Response(result, mimetype="application/json", status=200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/admin/qa_pairs')
def get_qa_pairs():
       with open('nlp/qa_pairs.json', encoding="utf8") as qa_pairs:
           data = json.load(qa_pairs)
           return jsonify(data)


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
    print('REPORTİNG QUESTİON')
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


def emit_chat_answer(sid, message):
    socketio.emit('chat answer', message, room=sid)

@socketio.on('connect')
def connect_message():
    print('socket io connected with id: ', request.sid)
    emit('chat answer', { 'answer': 'Merhaba, ben Metubot 🤖', 'finished': False })

    second_message = { 'answer': 'Sizlere nasıl yardımcı olabilirim?', 'finished': True }
    Timer(0.777, emit_chat_answer, (request.sid, second_message)).start()

@socketio.on('chat question')
def handle_question(msg):
    #print('question: ' + msg)
    answer = answerer.generatedAnswer(msg)
    emit('chat answer', { 'answer': answer, 'finished': True })


if __name__ == "__main__":
    print("NLP Backend api started. Ask your question with socket io")

    socketio.run(app, host="0.0.0.0", port="3000", debug=False, allow_unsafe_werkzeug=True)

