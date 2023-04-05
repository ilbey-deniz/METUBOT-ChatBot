import mysql.connector as Connect
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .mysql_helper import *

load_dotenv()

#  useful link for mysql.connector: https://linuxhint.com/cursor-execute-python/


class Connector:
    def __init__(self):
        self.host = os.getenv('MYSQL_HOST')
        self.user = os.getenv('MYSQL_USER')
        self.password = os.getenv('MYSQL_PASSWORD')
        self.database = None
        # add port if necessary
        self.connect()

    def connect(self):
        if self.database:
            self.con = Connect.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
            )
        else:
            self.con = Connect.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )

    def get_con(self):
        return self.con

    def get_cursor(self):
        self.connect()
        return self.con.cursor()

    def execute_query(self, query):  # it returns cursor
        self.connect()
        cursor = self.get_cursor()
        cursor.execute(query)
        return cursor

    def execute_query_and_commit(self, query):  # it execute and commit the query
        self.connect()
        cursor = self.con.cursor()
        cursor.execute(query)
        self.con.commit()
        cursor.close()

    def commit(self):
        self.connect()
        self.con.commit()

    def disconnect(self):
        self.con.close()

    def add_db(self, db_name):
        query = "CREATE DATABASE " + db_name
        self.execute_query_and_commit(query)


def create_db(db_name):
    connect_1 = Connector()
    try:
        connect_1.execute_query_and_commit(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        connect_1.execute_query_and_commit(f"USE {db_name};")
        return connect_1
    except Exception as e:
        print(e)
        print(f"error,can not create {db_name} database")
        return None


# *change this function later. Add db_name parameter.
def create_session():
    con = create_db(os.getenv('MYSQL_DATABASE'))
    con.database = os.getenv('MYSQL_DATABASE')
    if not con:
        print("session can not be created")
        return None
    engine = create_engine(f"mysql+mysqlconnector://{con.user}:{con.password}@{con.host}/{con.database}")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
