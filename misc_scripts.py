from backend.database.mysql.connector import *


  
def fix_asked_question_column_size():
    engine = get_engine()
    connection = engine.connect()
  
    
    table_name = 'asked_questions'

    query = f"ALTER TABLE {table_name} MODIFY asked_question TEXT"
    query = f"ALTER TABLE {table_name} MODIFY answer TEXT"
    

    connection.execute(query)



