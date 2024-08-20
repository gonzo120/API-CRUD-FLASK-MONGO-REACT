from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
import os
from dotenv import load_dotenv


# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
# Usar la variable de entorno MONGO_URI
app.config['MONGO_URI'] = 'mongodb+srv://gonzalezcontrerasnelson:12345@cluster0.hehrw.mongodb.net/pythonreactdb?retryWrites=true&w=majority'


mongo = PyMongo(app)
CORS(app)
db = mongo.db.users

@app.route('/')
def index():
    return '<h1>Pagina de inicio </h1>'

@app.route('/users', methods=['POST'])
def createUsers():
    id = db.insert_one({
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password'],
    })
    # Imprime el ID del documento insertado
    
    return jsonify(str(id.inserted_id))

@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id': str(doc['_id']),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password'],
        })
    return jsonify(users)

@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    user = db.find_one({"_id":ObjectId(id)})
    return jsonify({
        '_id':str(user['_id']),
        'name': user['name'],
        'email': user['email'],
        'password': user['password'],
    })

@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    user = db.find_one_and_delete({"_id":ObjectId(id)})
    return jsonify({'msg':'User Delected'})

@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
    userUpdate =  db.update_one({'_id': ObjectId(id)}, {"$set": {
    'name': request.json['name'],
    'email': request.json['email'],
    'password': request.json['password']
    }})
    return jsonify({'message': 'User Updated'})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)