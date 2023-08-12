import sqlite3 as sq

def db_request(connectionString, text):
   connect = sq.connect(connectionString)
   cursor = connect.cursor()
   
   cursor.execute(text)
   result = cursor.fetchall()
   
   connect.commit()
   
   return result