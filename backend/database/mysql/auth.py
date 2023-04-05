from .connector import *
from datetime import datetime, date, timedelta

def addUser(name, mail, password):
    session = create_session()
    if not session:
        print("user cant be added, session creation error")
        return False
    
    data = User(userName=name, userMail=mail, userPassword=password)
    
    try:
        session.add(data)
        session.commit()
        session.close()
        return True
    except Exception as e:
        session.close()
        return False
    

def getUserByMail(mail):
    session = create_session()
    if not session:
        print("session creation error")
        return {}
    ret = session.query(User).filter_by(userMail=mail).all()
    session.close()

    if not ret:
        return {}

    result = dict()
    result["name"] = ret[0].userName
    result["mail"] = ret[0].userMail

    return result


if __name__ == "__main__":
    addUser("isim2", "mail4", "pw1")
    addUser("isim2", "mail3", "pw1")
    getUserByMail("mail2")
    getUserByMail("isim2")

