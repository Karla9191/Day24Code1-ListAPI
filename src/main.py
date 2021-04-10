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

#***************Inicio del Get ***************#

@app.route('/todos', methods=['GET'])
def get_todos():

    # get all the people
    query = Todos.query.all()

    # map the results and your list of people  inside of the all_people variable
    all_todos = list(map(lambda x: x.serialize(), query))

    return jsonify(all_todos), 200

#***************Fin del Get ***************#

#***************Inicio del Post ***************#
@app.route('/add_todos', methods=['POST'])
def add_todos():

    request_body = request.get_json()
    todos = Todos(done=request_body["done"],label=request_body["label"])
    db.session.add(todos)
    db.session.commit()

    return jsonify("Se ha agregado correctamente"), 200

#***************Fin del Post ***************#

#***************Inicio del Delete ***************#
@app.route('/del_todos/<int:fid>', methods=['DELETE'])
def del_todos(fid):

    dtodo = Todos.query.get(fid)

    if dtodo is None:
        raise APIException('Todos not found', status_code=404)
    db.session.delete(dtodo)
    db.session.commit()

    return jsonify("Favorito eliminado de forma correcta."), 200
#***************Fin del Delete ***************#

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
