from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import pymongo

app = Flask(__name__)
# client = MongoClient('localhost', 27017)
# client = MongoClient('localhost', 27017, username='username', password='password')


client = pymongo.MongoClient("mongodb+srv://admin:Frite1234@cluster0.ybxsvft.mongodb.net/?retryWrites=true&w=majority")
db = client.test

db = client.flask_db
todos = db.todos


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        date = request.form['date']
        infos = request.form['infos']
        todos.insert_one({'content': content, 'degree': degree, 'date': date, 'infos': infos})
        return redirect(url_for('index'))
    all_todos = todos.find()
    important_todos = []
    unimportant_todos = []
    for todo in all_todos:
        if todo['degree'] == 'Important':
            important_todos.append(todo)
        else:
            unimportant_todos.append(todo)

    return render_template('index.html', important_todos=important_todos, unimportant_todos=unimportant_todos)
@app.post('/<id>/delete/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()