from backend.database.mysql.connector import Connector
from backend.database.mysql.mysql_helper import *

import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date, timedelta

DATABASE_NAME = "denemeQ"

# *Consider collecting all function into Class

def create_db(db_name):
    connect_1 = Connector()
    try:
        connect_1.execute_query_and_commit(f"CREATE DATABASE {db_name};")
        return connect_1
    except:
        print(f"error,can not create {db_name} database")
    try:
        connect_1.execute_query_and_commit(f"USE {db_name};")
        return connect_1
    except:
        print(f"error, unable to use {db_name}")


# *change this function later. Add db_name parameter.
def create_session():
    con = create_db(DATABASE_NAME)
    engine = create_engine(f"mysql+mysqlconnector://{con.user}:{con.password}@{con.host}/{DATABASE_NAME}")
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


def increase_question_count(question_id: int):
    session = create_session()
    session.query(Questions).filter_by(Qid=question_id).update({Questions.count: Questions.count + 1})
    session.flush()
    session.commit()
    session.close()


def increase_question_count_with_str(question: str):
    session = create_session()
    session.query(Questions).filter_by(question=question).update({Questions.count: Questions.count + 1})
    session.flush()
    session.commit()
    session.close()

# ?parameter can be converted to question instead of question_id
def update_question(question_id: int, question, answer, category):
    session = create_session()
    session.query(Questions).filter_by(Qid=question_id).update(
        {Questions.question: question, Questions.answer: answer, Questions.category: category})
    session.flush()
    session.commit()
    session.close()

# ?parameter can be converted to question instead of question_id
def delete_question_with_id(question_id: int):
    session = create_session()
    session.query(Questions).filter_by(Qid=question_id).delete()
    session.commit()
    session.close()


def get_most_frequent_questions(limit_count: int):
    session = create_session()
    res = session.query(Questions).order_by(desc(Questions.count)).limit(limit_count).all()
    result_list = []
    for r in res:
        temp = dict()
        temp["id"] = r.Qid
        temp["question"] = r.question
        temp["answer"] = r.answer
        temp["category"] = r.category
        temp["count"] = r.count
        result_list.append(temp)
    return result_list


# TODO: get most liked/disliked questions
def get_most_liked_questions(limit_count: int):
    session = create_session()


# get disliked/liked feedbacks
def advance_query_feedbacks(is_liked: bool, min_similarity=0.0, max_similarity=1.0):
    is_liked = 1 if is_liked else 0
    session = create_session()
    res = session.query(Questions, Feedbacks). \
        select_from(Questions).join(Feedback_activity).join(Feedbacks).filter(
        Questions.Qid == Feedback_activity.Qid
    ).filter(
        Feedbacks.Fid == Feedback_activity.Fid
    ).filter(Feedbacks.is_liked == is_liked).filter(
        Feedbacks.similarity >= min_similarity).filter(Feedbacks.similarity <= max_similarity).all()
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


# TODO: get avg like/dislike ratio

# get avg similarity
def get_average_similarity():
    session = create_session()
    res = session.query(func.avg(Feedbacks.similarity)).scalar()
    return res


# TODO: get most feedback taken question (res <= feedback count/question count)

# get feedback in (X days)
def get_feedbacks_with_time(day_count: int):
    '''
    get all the feedbacks in last X day, where X is day_count parameter.
    :param day_count: total # of passed day from current day.
    :return: feedback datas within specified days.
    '''
    query_date = date.today() + timedelta(days=-day_count)
    print(query_date)
    session = create_session()
    res = session.query(Questions, Feedbacks). \
        select_from(Questions).join(Feedback_activity).join(Feedbacks).filter(
        and_(Feedbacks.Fid == Feedback_activity.Fid), Questions.Qid == Feedback_activity.Qid
    ).filter(
        func.date(Feedback_activity.created_at) >= query_date
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


def query_all_questions():
    session = create_session()
    res = session.query(Questions).all()
    results = []
    for r in res:
        temp = dict()
        temp["id"] = r.Qid
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

    increase_question_count(12)
    increase_question_count_with_str("saat kaç")
    increase_question_count_with_str("saat kaç")
    increase_question_count_with_str("saat kaç")
    increase_question_count_with_str("saat kaç")
    r = get_most_frequent_questions(2)
    print(r)

    a_q_f = advance_query_feedbacks(True, 0.2, 0.81)
    print(a_q_f)

    avg_similarity = get_average_similarity()
    print(avg_similarity)

    feedback_w_day = get_feedbacks_with_time(7)
    print(feedback_w_day)
