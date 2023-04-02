from connector import *
from datetime import datetime, date, timedelta

def addUser(name, mail, password):
    session = create_session()
    if not session:
        print("user cant be added, session creation error")
        return None
    
    data = User(userName=name, userMail=mail, userPassword=password)
    
    try:
        session.add(data)
        session.commit()
        session.close()
        return True
    except Exception as e:
        print(e)
    
    session.close()
    return False

if __name__ == "__main__":
    addUser("isim2", "mail2", "pw1")