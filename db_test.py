import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="chess"
)

cursor = conn.cursor()
                                                                                           
cursor.execute("INSERT INTO PLAYERS (ID,FIRSTNAME) VALUES (24,'Ravi')")                   ##inserting data
conn.commit()

cursor.execute("SELECT * FROM PLAYERS")                                           ##selecting data

rows=cursor.fetchall()
for row in rows:
    print(row)

conn.close()