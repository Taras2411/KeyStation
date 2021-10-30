from getpass import getpass
import mysql.connector 
import os

mydb = mysql.connector.connect(
    host="localhost",
    port='3306',
    user="admin",
    password=os.environ['DBPASSWORD'],
    database="key_station")
    
        
        
mycursor = mydb.cursor()
card1 = '699451644659'
sql = f"SELECT FIO FROM key_station.Cards JOIN key_station.Teachers ON key_station.Cards.TeacherId = key_station.Teachers.id WHERE Card IN ({card1})"




mycursor.execute(sql)

myresult = mycursor.fetchall()

for x in myresult:
    print(x)
