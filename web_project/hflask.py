from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import pickle
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hello/')
@app.route('/hello/<name>')
def bighello(name=None):
    return render_template('hello.html', name=name)

@app.route('/todo_list', methods=['POST', 'GET'])
def submit_todo():
    db = read_db()
    if request.method == "POST":
        data = request.form.to_dict()
        if not data["todo_item"].lower() in map(lambda x: x.lower(), db):
            db.append(data["todo_item"])
        save_db(db)
    return render_template('todo.html', db=db)

@app.route('/delete', methods=['POST', 'GET'])
def delete():
    db = read_db()
    if request.method == "POST":
        to_delete = request.form.to_dict()["task"]
        db.remove(to_delete)
        save_db(db)
    return redirect("/todo_list")

@app.route('/important', methods=['POST', 'GET'])
def important():
    db = read_db()
    if request.method == "POST":
        entry = request.form.to_dict()["task"]
        db.remove(entry)
        db.append(entry.upper())
        save_db(db)
    return redirect("/todo_list")

@app.route('/low_priority', methods=['POST', 'GET'])
def low_priority():
    db = read_db()
    if request.method == "POST":
        entry = request.form.to_dict()["task"]
        db.remove(entry)
        db.append(entry.lower())
        save_db(db)
    return redirect("/todo_list")

def read_db():
    if os.path.isfile("db.pickle"):
        with open("db.pickle", "rb") as f:
            return pickle.load(f)
    else:
        return []

def save_db(db):
    with open('db.pickle', 'wb') as f:
        pickle.dump(db, f)

if __name__ == '__main__':
    app.run(debug = True)
