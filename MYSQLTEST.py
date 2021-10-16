from getpass import getpass
import mysql.connector 

mydb = mysql.connector.connect(
    host="103.167.136.18",
    port='11004',
    user="root",
    password="OHAxrk22735",
    database="key_statyion")
    
        
        
mycursor = mydb.cursor()
sql = "SELECT Card, en FROM key_statyion.Cards JOIN key_statyion.Names_cards ON key_statyion.Cards.id = key_statyion.Names_cards.Card_id JOIN key_statyion.Names ON key_statyion.Names_cards.Name_id = key_statyion.Names.id WHERE name IN ('Ivan')"
        
mycursor.execute(sql)

myresult = mycursor.fetchall()

for x in myresult:
    print(x)