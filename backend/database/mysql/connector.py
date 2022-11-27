import mysql.connector as Connect
import os
from dotenv import load_dotenv
load_dotenv()

#  useful link for mysql.connector: https://linuxhint.com/cursor-execute-python/


class Connector:
    def __init__(self, database=None):
        self.host = os.getenv('HOST')
        self.user = os.getenv('USER')
        self.password = os.getenv('PASSWORD')
        # add port if necessary
        self.database = database
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


# connect_1 = Connector("Mefebe")

# connect_1.execute_query_and_commit("CREATE TABLE Person ("
#                                    "PersonID int,"
#                                    "LastName varchar(255),"
#                                    "FirstName varchar(255),"
#                                    "City varchar(255));")
#
#
# query = ('INSERT INTO Person (PersonID, LastName, FirstName, City) VALUES (%s, %s, %s, %s)')
# vals = [
#         (1, "Ali", "Veli", "Ankara"),
#         (2, "Amat", "Saygıç", "Ankara"),
#         (3, "Memet", "Maraz", "Konya"),
#         (4, "Dumrul", "Deli", "Ankara"),
#         (5, "Bekir", "Limon", "Kayseri"),
#         (6, "Temel", "Semir", "Ankara")
#        ]

#
# cursor = connect_1.get_cursor()
#
# cursor.executemany(query, vals)
#
# connect_1.con.commit()

# conn = connect_1.get_con()
#
# mycursor = conn.cursor()
#
# query = 'INSERT INTO MOVIE (id, name, year) VALUES (%s, %s, %s)'
# val = [(2, "Kung Fu panda", 2014),
#        (4, "Frozen", 2014),
#        (5, "Frozen2", 2020),
#        (6, "Iron Man", 2013)
#
#        ]
#
# mycursor.executemany(query,val)
#
# conn.commit()




