from backend.database.mysql.connector import *

import json
from datetime import datetime, date, timedelta

def addUser(name, mail, password):
    session = create_session()
    q = session.query(User).filter(User.userMail==mail)
    session.query(q.exists())
    #if exists do not add

    
    data = User(userName=name, userMail=mail, userPassword=password)
    session.add(data)
    session.commit()
    session.close()
