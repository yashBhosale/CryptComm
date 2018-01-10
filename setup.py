import sys
import sqlite3

db = sqlite3.connect('users.db')
cursor = db.cursor()

cursor.execute("CREATE TABLE Users(Username TEXT	PRIMARY KEY 	NOT NULL, Password TEXT	NOT NULL, IP_ADDR TEXT);")

print "table created sucessfully";
db.close()