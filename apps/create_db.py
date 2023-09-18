import mysql.connector

mydb = mysql.connector.connect(
    host="103.139.175.14",
    user="erg39721_ergocust",
    password="ergocust.com",
    )

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE erg39721_ergocust")

my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
    print(db)