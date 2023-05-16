from backend.database.mysql.connector import *


  

session = create_session()
  
table_name = 'asked_questions'

query = f"ALTER TABLE {table_name} MODIFY asked_question TEXT"
query = f"ALTER TABLE {table_name} MODIFY answer TEXT"

session.execute(query)

session.commit()
session.close()