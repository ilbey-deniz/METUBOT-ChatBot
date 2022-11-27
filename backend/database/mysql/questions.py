from backend.database.mysql.connector import Connector


def create_question_db():
    try:
        connect_1 = Connector()

        connect_1.execute_query_and_commit("CREATE DATABASE questions;")
    except:
        pass

    try:
        connect_1.execute_query_and_commit("USE questions;")
    except:
        pass


def drop_table():
    try:
        connect_1 = Connector("questions")
        connect_1.execute_query_and_commit("drop table Questions;")
    except:
        pass


def create_table():
    try:
        connect_1 = Connector("questions")
        connect_1.execute_query_and_commit(
            "CREATE TABLE Questions ("
            "Question varchar(255),"
            "Matched_question varchar(255),"
            "Similarity float,"
            "PRIMARY KEY (Question));")
    except:
        pass


def insert_question(question, matched_question, similarity):
    try:
        connect_1 = Connector("questions")

        query = ('INSERT INTO Questions (Question, Matched_question, Similarity) VALUES (%s, %s, %s)')
        vals = [
            (question, matched_question, similarity)
        ]
        cursor = connect_1.get_cursor()

        cursor.executemany(query, vals)

        connect_1.con.commit()
    except:
        pass


def get_query_result(query):
    try:
        connect_1 = Connector("questions")
        res = connect_1.execute_query(query)
        result = []
        for r in res:
            result.append(r)
    except:
        result = []
    return result


# insert_question("trial", "test", 0.97)

# some test queries


res = get_query_result(
    "select * from questions;"
)
print(res)

res_2 = get_query_result(
    "select q.question"
    " from questions q"
    " where q.similarity <= 0.5;"
)

print(res_2)

res_3 = get_query_result(
    "select q.Matched_question, avg(q.Similarity)"
    " from questions q"
    " where q.Matched_question = 'ücretsiz Autocad kullanmak için ne yapmam lazım'"
    " group by q.Matched_question"
)
print(res_3)
