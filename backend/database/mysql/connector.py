import mysql.connector as Connect
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.mysql.mysql_helper import *

load_dotenv()

#  useful link for mysql.connector: https://linuxhint.com/cursor-execute-python/


class Connector:
    def __init__(self, database=None):
        self.host = os.getenv('HOST')
        self.user = os.getenv('USER')
        self.password = os.getenv('PASSWORD')
        if not database:
            self.database = os.getenv('DATABASE')
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
    con = create_db()
    engine = create_engine(f"mysql+mysqlconnector://{con.user}:{con.password}@{con.host}/{con.database}")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
