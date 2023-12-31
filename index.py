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
import bcrypt


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

@app.route('/addQuestion', methods = ['POST'])
#@token_required
def add_question():

    args = request.get_json()
    category = args["category"]
    question = args["questions"]
    answer = args["answers"]
    buttons = args["buttons"]

    if None in [question,answer,category]:
        return response(status="error", message="invalid question, category or answer", code=400)

    print("ADD QUESTION: ")
    print(f"Category: {category}")
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print(f"Buttons: {buttons}")

    res = answerer.addQuestion(question, answer, category, buttons) #Note that question and answer are expected to be given as lists. These square brackets are temporary

    return response(status="success", message="question added", data=res)

@app.route('/deleteQuestion', methods = ['DELETE'])
#@token_required
def delete_question():
    question_id = request.args.get("question_id")

    print('DELETE QUESTION: ')
    print(f'Answer ID: {question_id}')

    answerer.deleteAnswer(question_id)

    return response(status="success", message="question deleted")

@app.route('/updateQuestion', methods = ['POST'])
#@token_required
def update_question():
    args = request.get_json()
    id = args["id"]
    category = args["category"]
    question = args["questions"]
    answer = args["answers"]
    buttons = args["buttons"]

    if None in [question, answer, category]:
        return response(status="error", message="invalid question, category or answer", code=400)

    print('UPDATE QUESTION: ')
    print(f"Answer ID: {id}")
    print(f"Category: {category}")
    print(f"Question: {question}")
    print(f"Answer: {answer}")

    res = answerer.updateAnswer(id, question, answer, category, buttons)

    #response_message = json.dumps(response_message, indent=4, ensure_ascii=False)
    #response = Response(response_message, mimetype="application/json", status=200)
    #response.headers.add('Access-Control-Allow-Origin', '*')
    return response(status="success", message="question updated", data=res)

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
    data = answerer.getPage(0,10000)
    return jsonify(data)
    #with open('nlp/qa_pairs.json', encoding="utf8") as qa_pairs:
        #data = json.load(qa_pairs)
        #return jsonify(data)


@app.route('/getAllQuestions')
def get_all_questions():
    query_res = query_all_questions()
    result = dict()
    result["data"] = query_res

    result = json.dumps(result, indent=4, ensure_ascii=False)
    response = Response(result, mimetype="application/json", status=200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/addFeedback')
def report_questions():
    print('REPORTİNG QUESTİON')
    asked_question_id = request.args.get("asked_question_id")
    report_message = request.args.get("report_message")
    is_liked = request.args.get("is_liked")

    add_feedback(int(asked_question_id), is_liked, report_message)
    response_message = json.dumps("feedback is added", indent=4, ensure_ascii=False)
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
def handle_question(q):
    answer = answerer.generatedAnswer(q)
    qid = add_asked_question(q, answer.text["question"], answer.similarity, answer.category)
    emit('chat answer', { 'answer': answer.text, 'finished': True, 'asked_question_id': qid })

@app.route("/ask")
def ask_endpoint():
    q = request.args.get("question")
    answer = answerer.generatedAnswer(q)
    qid = add_asked_question(q, answer.text["question"], answer.similarity, answer.category)
    return response(status="success", data=answer.text)

@app.route("/askedQuestions")
def get_asked_questions_route():
    return response(status="success", data=get_asked_questions())


@app.route("/upload_excel", methods = ['POST'])
def upload_excel():
    if 'file' not in request.files:
        return "No file uploaded"
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        print(f'File {filename} uploaded successfully!')

        data = add_questions_from_excel(qpath=file)

        if data is None:
            pass # Not Excel
        else:
            answerer.initFromDict(data)

    return response("success", 200)

def check_password_hash(pw_hash, password):
    return bcrypt.checkpw(password.encode('utf-8'), pw_hash.encode('utf-8'))

@socketio.on("token check")
def token_check(token):
    if not token:
        emit("token check answer", {"status": "error", "message": "Missing token"})


    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
        user = getUserByMail(data['sub'])
    except:
        emit("token check answer", {"status": "error", "message": "Token is expired."})
        return
    if not user:
        emit("token check answer", {"status": "error", "message": "User not found."})
    elif data["exp"] < datetime.utcnow().timestamp():
        emit("token check answer", {"status": "error", "message": "Token is expired."})
    else:
        emit("token check answer", {"status": "success", "message": "Token is valid."})


@socketio.on("login")
def login(msg):

    if not msg or not msg["mail"] or not msg["password"]:
        emit("login answer", {"status": "error", "message": "missingCredentials"})
        return

    user = getUserByMail(msg["mail"])

    if not user:
        emit("login answer", {"status": "error", "message": "noSuchUser"})
        return

    if check_password_hash(user["password"], msg["password"]):
        token = jwt.encode({'sub': user["mail"], 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return emit("login answer", {'status':"success", 'token': token.decode('UTF-8')})

    return emit("login answer", {"status": "error", "message": "wrongPassword"})


@socketio.on("register")
def register(msg):
    try:
        username = msg["username"]
        mail = msg["mail"]
        password = msg["password"]
    except:
        emit("register answer", {"status": "error", "message": "missingCredentials"})


    if not mail or not username or not password:
        emit("register answer", {"status": "error", "message": "missingCredentials"})

    user = getUserByMail(mail)
    if user:
        emit("register answer", {"status": "error", "message": "userExists"})

    if addUser(username, mail, password):
        token = jwt.encode({'sub': mail, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        emit("register answer", {'status':"success", 'token': token.decode('UTF-8')})
    emit("register answer", {"status": "error", "message": "unknownError"})


@app.route("/secret")
@token_required
def getProtected():
    return response("secret test endpoint", 200)


if __name__ == "__main__":
    print("NLP Backend api started. Ask your question with socket io")

    socketio.run(app, host="0.0.0.0", port="3000", debug=True, allow_unsafe_werkzeug=True)

