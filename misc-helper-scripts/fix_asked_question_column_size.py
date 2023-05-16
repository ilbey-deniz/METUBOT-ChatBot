from backend.database.mysql.connector import *


  

session = create_session()
  
table_name = 'asked_questions'
  # change varchar to text
query = f"ALTER TABLE {table_name} MODIFY COLUMN question TEXT"
query = f"ALTER TABLE {table_name} MODIFY COLUMN answer TEXT"
session.execute(query)



session.commit()
session.close()