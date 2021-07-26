import pandas as pd
import sqlite3 as sq3
import json as jsn
from flask import Flask
from pandas.io.sql import execute

app = Flask(__name__)

@app.route("/videos")
def videos():
    con = sq3.connect('frttt.db')
    cur = con.cursor()
    todos = list(cur.execute('Select * from videos'))
    todos_string = jsn.dumps(todos)
    return (todos_string)


@app.route('/videos/<video_id>')
def show_video_information(video_id):
    con = sq3.connect('frttt.db')
    cur = con.cursor()
    todos = list(cur.execute('Select * from videos where ID = {}'.format(video_id)))
    if len (todos) == 0:
        return 'Ops, não consegui encontrar o vídeo que você está procurando!'
    else: 
        todos_video_id = jsn.dumps(todos[0])
        return (todos_video_id)

from flask import request

@app.route('/videos/<video_id>', methods=['DELETE'])
def delete_video(video_id):
    con = sq3.connect('frttt.db')
    cur = con.cursor()
    todos = cur.execute('DELETE FROM videos WHERE ID = {}'.format(video_id))
    con.commit()
    video_deletado = todos.rowcount
    if video_deletado == 0:
        return 'Ops, o vídeo selecionado não pôde ser deletado. Você colocou o vídeo certo?'
    else: 
        return 'Seu vídeo foi deletado com sucesso!'

@app.route('/videos', methods=['POST'])
def novo_video():
    error = None
    if validate_payload(request.form['Título'],
                    request.form['Descrição'],
                    request.form['URL']):
        con = sq3.connect('frttt.db')
        cur = con.cursor()
        maximo_id = list(cur.execute ('Select MAX (ID) from videos'))
        novo_id = maximo_id[0][0] + 1
        cur.execute("INSERT INTO videos VALUES ({}, '{}', '{}', '{}')".format(
            novo_id, request.form['Título'], request.form['Descrição'], request.form['URL']
        ))
        con.commit()
        con.close ()
        return show_video_information(novo_id)

def validate_payload(title, description, url): 
    if not isinstance (title, str):
        return False
    if len (title) == 0:
        return False
    if len (title) >= 50:
        return False
    if not isinstance (description, str):
        return False
    if len (description) == 0:
        return False
    if len (description) >= 150:
        return False
    if not isinstance (url, str):
        return False
    if len (url) == 0:
        return False
    if len (url) >= 200:
        return False
    return True