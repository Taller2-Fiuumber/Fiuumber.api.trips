from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import os


app = Flask(__name__)

app.config["MONGO_URI"] = 'mongodb://' +\
    os.environ['MONGO_INITDB_ROOT_USERNAME'] + ':' +\
    os.environ['MONGO_INITDB_ROOT_PASSWORD'] + '@' +\
    os.environ['MONGODB_HOSTNAME'] + ':27017/' +\
    os.environ['MONGO_INITDB_DATABASE']

mongo = PyMongo(app)

@app.route("/")
def home():
    return "Hello, world"


@app.route('/todo')
def todo():
    _todos = mongo.db.todo.find()

    item = {}
    data = []
    for todo in _todos:
        item = {
            'id': str(todo['_id']),
            'todo': todo['todo']
        }
        data.append(item)

    return jsonify(
        status=True,
        data=data
    )

@app.route('/todo', methods=['POST'])
def createTodo():
    data = request.get_json(force=True)
    item = {
        'todo': data['todo']
    }
    mongo.db.todo.insert_one(item)

    return jsonify(
        status=True,
        message='To-do saved successfully!'
    ), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.env['PORT'])

