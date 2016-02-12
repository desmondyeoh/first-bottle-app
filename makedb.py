__author__ = 'desmond'

import sqlite3
con = sqlite3.connect('todo.db')
con.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(100) NOT NULL, status bool NOT NULL)")
con.execute("INSERT INTO todo (task,status) VALUES ('Read-a-byte of python to get a good introduction to python',0)")
con.execute("INSERT INTO todo (task, status) VALUES ('Visit the Python website', 1)")
con.execute("INSERT INTO todo (task, status) VALUES ('Test various editors and check the syntax highlighting', 1)")
con.execute("INSERT INTO todo (task, status) VALUES ('Choose your favourite WSGI-Framework', 0)")
con.commit() # REMEMBER THIS!!!