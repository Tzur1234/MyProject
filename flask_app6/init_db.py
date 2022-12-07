# a build in module to connect with sqlite

import sqlite3

# open new data base called 'database.db'
# creat an object to speak with the db
db = sqlite3.connect('database.db')

#open sql file called 'f' and read the content from it
with open('schema.sql') as f:
    str = f.read()
    # execute the creating new db query 
    db.executescript(str)  


cur = db.cursor()
# Insert new content

cur.execute("INSERT INTO posts (title, content) VALUES (?,?)", ("first-title", "first-comment-first"))

db.commit()
db.close()







