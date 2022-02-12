
from flask import Flask, jsonify, request, Response 

from flask_pymongo import PyMongo

from werkzeug.security import generate_password_hash, check_password_hash

from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] ='mongodb://localhost/pythonmongodb'

mongo = PyMongo(app)

@app.route('/users', methods=['GET'])
def get_users():
    users=mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['GET'])
def get_a_user(id):
    user = mongo.db.users.find_one({'_id':ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype="applicacion/jason")

@app.route('/users', methods=['POST'])
def create_user():
    #receiving data
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    #saving data
    if name and email and password:
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert({
            'name':name,
            'email': email,
            'password': hashed_password
        })
        response = {
            'id': str(id),
            'name':name,
            'email':email,
            'password':hashed_password
        }
        return response
    else:
        {"message":"received"}
    return jsonify({'message':'received'})

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id':ObjectId(id)})
    response = jsonify({'message': 'User'+ id + 'was deleted'})
    return response

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    #receiving data
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    
    #updating data
    if name and email and password: 
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one(
            {'_id': ObjectId(id)},
            { '$set':{
                'name':name,
                'email':email,
                'password': hashed_password
            }})
        response = jsonify({'message': 'user' + id + 'was updated'})
        return response
    return jsonify({'message': 'user not found'})


# @app.errorhadler(404)
# def not_found(error=None):
#     jsonify({
#       
#       })
#     message={
#         'message': 'Resource not found'+ request.url,
#         'status':404
#     }
#     return response

if __name__=="__main__":
    app.run(debug=True)