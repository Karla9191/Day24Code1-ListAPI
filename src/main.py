"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Todos
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

#Ruta para Todos del proyeto List
@app.route('/get_todos', methods=['GET'])
def get_todos():

    # get all the people
    query = Todos.query.all()

    # map the results and your list of people  inside of the all_people variable
    all_todos = list(map(lambda x: x.serialize(), query))

    return jsonify(all_todos), 200




#Get - Post - Put - Delete

@app.route('/get_todos', methods=['GET'])
def get_listado():

    # get all the people
    query = Todos.query.all()

    # map the results and your list of people  inside of the all_people variable
    all_listados = list(map(lambda x: x.serialize(), query))

    return jsonify(all_listados), 200

@app.route('/add_todos', methods=['POST'])
def add_listado():

    request_body = request.get_json()
    listado = Todos(done=request_body["done"],id=request_body["id"],label=request_body["label"])
    db.session.add(listado)
    db.session.commit()

    return jsonify("Se ha agregado correctamente"), 200

@app.route('/upd_todos/<int:fid>', methods=['PUT'])
def upd_listado(fid):

    listado = Todos.query.get(fid)
    if listado is None:
        raise APIException('No encontrado', status_code=404)

    request_body = request.get_json()

    if "label" in request_body:
        listado.label = request_body["label"]

    db.session.commit()
    return jsonify("Modificado correctamente"), 200

@app.route('/del_todos/<int:fid>', methods=['DELETE'])
def del_listado(fid):

    listado = Todos.query.get(fid)

    if listado is None:
        raise APIException('No encontrado', status_code=404)
    db.session.delete(listado)
    db.session.commit()

    return jsonify("Eliminado correctamente"), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
