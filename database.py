import psycopg2

connection = psycopg2.connect(
    database="記中",
    user="學號",
    password="密碼",
    host="",
    port="8000")

cursor = connection.cursor()
cursor.execute("CREATE TABLE userdata (id serial PRIMARY KEY, name VARCHAR(50),userid VARCHAR(50));")
cursor.close()