import pandas as pd
import sqlite3 as sq3
import json as jsn
from flask import Flask

app = Flask(__name__)

@app.route("/videos")
def videos():
    con = sq3.connect('frttt.db')
    cur = con.cursor()
    todos = list(cur.execute('Select * from videos'))
    todos_string = jsn.dumps(todos)
    return (todos_string)


