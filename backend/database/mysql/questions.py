from backend.database.mysql.connector import Connector
from backend.database.mysql.mysql_helper import *

import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime


# *Consider collecting all function into Class

def create_db(db_name):
    connect_1 = Connector()
    try:
        connect_1.execute_query_and_commit(f"CREATE DATABASE {db_name};")
    except:
        print(f"error,can not create {db_name} database")
    try:
        connect_1.execute_query_and_commit(f"USE {db_name};")
    except:
        print(f"error, unable to use {db_name}")


# *change this function later. Add db_name parameter.
def create_session():
    create_db("denemeQ")
    engine = create_engine("mysql+mysqlconnector://root:miniklim10@localhost/denemeQ")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def add_question(question, answer, category):
    session = create_session()
    count = 0
    data = Questions(question=question, answer=answer, category=category, count=count)
    session.add(data)
    session.commit()
    session.close()


def add_multiple_questions(path):
    '''
    The function add questions from the data as a json to the database.
    it insert the all data as fast as possible with the help of the bulk_insertion.
    :param path: path to json data
    :return: None
    '''

    f = open(path, 'r', encoding='UTF-8')
    data = json.load(f)

    session = create_session()

    session.bulk_save_objects(
        [Questions(question=d['question'][0], answer=d['answer'][0],
                   category=d['category'], count=0) for d in data["qa-pairs"]]
    )
    session.commit()
    session.close()


def add_multiple_questions_from_json(json_data):
    '''
    The function add questions directly from json data.
    it insert the all data as fast as possible with the help of the bulk_insertion.
    :param json_data: provided json data
    :return: None
    '''

    data = json.load(json_data)

    session = create_session()

    session.bulk_save_objects(
        [Questions(question=d['question'][0], answer=d['answer'][0],
                   category=d['category'], count=0) for d in data["qa-pairs"]]
    )
    session.commit()
    session.close()


def delete_question_with_id(question_id: int):
    session = create_session()
    session.query(Questions).filter_by(id=question_id).delete()
    session.commit()
    session.close()


def query_all_questions():
    session = create_session()
    res = session.query(Questions).all()
    results = []
    for r in res:
        temp = dict()
        temp["question"] = r.question
        temp["answer"] = r.answer
        temp["category"] = r.category
        temp["count"] = r.count
        results.append(temp)
    return results


def add_feedback(main_question_id, similarity, asked_question, is_liked, report_message):
    session = create_session()
    feedback = Feedbacks(asked_question=asked_question, similarity=similarity,
                         is_liked=is_liked, report_message=report_message)
    session.add(feedback)
    session.commit()

    feedback_activity = Feedback_activity(Qid=main_question_id, Fid=feedback.Fid, created_at=datetime.now())
    session.add(feedback_activity)
    session.commit()
    session.close()


def query_all_feedbacks():
    session = create_session()
    res = session.query(Questions, Feedbacks).\
        select_from(Questions).join(Feedback_activity).join(Feedbacks).filter(
        Questions.Qid == Feedback_activity.Qid
    ).filter(
        Feedbacks.Fid == Feedback_activity.Fid
    ).all()
    results = []
    for q, f in res:
        temp = dict()
        temp["asked_question"] = f.asked_question
        temp["question"] = q.question
        temp["similarity"] = f.similarity
        temp["is_liked"] = f.is_liked
        temp["report_message"] = f.report_message
        results.append(temp)

    return results


if __name__ == "__main__":

    add_question("sa", "as", "selamlama")

    add_multiple_questions(path="../../../Elasticsearch/qa_pairs.json")

    results = query_all_questions()

    for result in results:
        print(f"({result['question']}, \n{result['answer']},"
              f" {result['category']}, \n{result['count']})")

    add_feedback(1, 0.7, "Naber", True, "gayet güzel cevap döndü")
    add_feedback(6, 0.2, "şifremi unuttum",  False, "berbat bir cevap, umduğumu bulamadım")
    add_feedback(12, 0.8, "yemeeeek",  True, "tam istediğim gibi yemek listesine erişebildim.")

    a = query_all_feedbacks()
    print(a)
