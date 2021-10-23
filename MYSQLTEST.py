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
sql = "SELECT Card, en FROM key_station.Cards JOIN key_station.Names_cards ON key_station.Cards.id = key_station.Names_cards.Card_id JOIN key_station.Names ON key_station.Names_cards.Name_id = key_station.Names.id WHERE name IN ('Ivan')"
        
mycursor.execute(sql)

myresult = mycursor.fetchall()

for x in myresult:
    print(x)
