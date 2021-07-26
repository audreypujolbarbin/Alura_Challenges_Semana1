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