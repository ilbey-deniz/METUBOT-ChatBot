from flask import Flask, jsonify, request, Response, render_template
import pandas
from werkzeug.utils import secure_filename
import json
from flask_socketio import SocketIO, send, emit
from threading import Timer
from DummyAnswerer import DummyAnswerer
from Answerer import Answerer
from AnswerGeneratorMetu import AnswerGeneratorMetu
from data.metu.json_qapairs_manager import add_questions_manually, add_questions_from_excel
from backend.database.mysql.questions import *
from backend.database.mysql.auth import *
import nlp.elastic as elastic

from functools import wraps
import jwt


answer_generator = AnswerGeneratorMetu()

#answerer: Answerer = FasttextAnswerer(answer_generator)
answerer: Answerer = elastic.ElasticsearchInterface(answer_generator)
#answerer: Answerer = DummyAnswerer(answer_generator)

app = Flask(__name__,
            static_folder = "./frontend/dist/static",
            template_folder = "./frontend/dist")

app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)
def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        user_not_found_msg = {
            'message': 'No such user with the provided email.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user = getUserByMail(data['sub'])
            # still need to check whether the user using the token still exists or not
            if not user:
                return jsonify(user_not_found_msg), 401
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify

#status can be either success or error
def response(status, data=None, message=None, code=200):
    response = jsonify({"status":status, "data":data, "message":message})
    return response, code

## routes start here
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/addQuestion')
def add_one_questions():
    print('ADDING QUESTION')
    category = request.args.get("category")
    question = request.args.get("question")
    answer = request.args.get("answer")
    if None in [question,answer,category]:
        return response(status="error", message="invalid question, category or answer", code=400)

    print(category, question, answer)
    #add_question(question, answer, category)
    answerer.addQuestion([question], [answer], category) #Note that question and answer are expected to be given as lists. These square brackets are temporary

    return response("success")

@app.route('/deleteQuestion')
def delete_one_questions():
    print('QUESTION IS DELETING')
    question_id = request.args.get("question_id")
    delete_question_with_id(int(question_id))

    return response(status="success", message="question is deleted")

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
    #add_asked_question(msg, answer, 1234, 'kategori?')
    emit('chat answer', { 'answer': answer, 'finished': True })

@app.route("/ask")
def ask_endpoint():
    q = request.args.get("question")
    answer = answerer.generatedAnswer(q)
    #add_asked_question(msg, answer, 1234, 'kategori?')
    return response(status="success", data=answer)

@app.route("/askedQuestions")
def get_asked_questions_route():
    return response(status="success", data=get_asked_questions())


@app.route("/add-excel", methods = ['POST'])
def add_excel():
    file = request.files['file']
    add_questions_from_excel(file)
    return response("success", 200)



@app.route("/secret")
@token_required
def getProtected():
    return response("secret test endpoint", 200)


if __name__ == "__main__":
    print("NLP Backend api started. Ask your question with socket io")

    socketio.run(app, host="0.0.0.0", port="3000", debug=False, allow_unsafe_werkzeug=True)

