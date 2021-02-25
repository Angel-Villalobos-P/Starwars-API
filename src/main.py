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
from models import db, User, Planet, Character, Favorite
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

############## Endpoints para usuarios ##############
@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.all();
    results = list(map(lambda x: x.serialize(), users))

    #=====================================================================
    # En caso que se necesite mostrar la info de cada favorito dentro del user, seguir esta lógica
    #info = results[0]["favorites"]
    #planet = Planet.query.get(info[0]["planet_id"])
    #return jsonify(results, info, planet.serialize()), 200
    #=====================================================================

    return jsonify(results), 200

# Obtiene un user especifico
@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):

    user = User.query.get(id)
    if user is None:
        raise APIException('User not found', status_code=404)

    return jsonify(user.serialize()), 200

# Favoritos del usuario
@app.route('/users/<int:id>/favorites', methods=['GET'])
def get_userFavorite(id):

    user = User.query.get(id).serialize()
    if user is None:
        raise APIException('User not found', status_code=404)

    userFavorites = user["favorites"]
    favs = list(map(lambda x: x, userFavorites))

    return jsonify(favs), 200

@app.route('/add_user', methods=['POST'])
def add_user():

    # recibir info del request
    request_body = request.get_json()
    print(request_body)

    new_user = User(name=request_body["name"], username=request_body["username"], password=request_body["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify("All good, added"), 200

# Agrega un favorito al usuario
@app.route('/users/<int:id>/favorites', methods=['POST'])
def add_userFavorite(id):

    fav_to_add = request.get_json()
    user = User.query.get(id).serialize()
    
    if user is None:
        raise APIException('User not found', status_code=404)

    new_favorite = Favorite(user_id=id, planet_id=fav_to_add["planet_id"], character_id=fav_to_add["character_id"])
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify("All good, added"), 200





############## Endpoints para planetas ##############
@app.route('/planets', methods=['GET'])
def get_planets():
    # get all the todos
    planets = Planet.query.all()

    # map the results and your list of todos  inside of the all_todos variable
    results = list(map(lambda x: x.serialize(), planets))

    return jsonify(results), 200

# Obtiene un planeta especifico
@app.route('/planet/<int:id>', methods=['GET'])
def get_planet(id):

    planet = Planet.query.get(id)
    if planet is None:
        raise APIException('Planet not found', status_code=404)

    return jsonify(planet.serialize()), 200

@app.route('/add_planet', methods=['POST'])
def add_planet():

    # recibir info del request
    request_body = request.get_json()
    print(request_body)

    new_planet = Planet(name=request_body["name"], climate=request_body["climate"], diameter=request_body["diameter"],
        gravity=request_body["gravity"], population=request_body["population"], terrain=request_body["terrain"])

    db.session.add(new_planet)
    db.session.commit()

    return jsonify("All good, added: ", new_planet.serialize()), 200

@app.route('/update_planet/<int:id>', methods=['PUT'])
def update_planet(id):

    body = request.get_json()
    planet = Planet.query.get(id)

    if planet is None:
        raise APIException('Planet not found', status_code=404)
    if body is None:
        raise APIException('Wrong data', status_code=404)

    if "name" in body:
        planet.name = body["name"]
    if "climate" in body:
        planet.climate = body["climate"]
    if "diameter" in body:
        planet.diameter = body["diameter"]
    if "gravity" in body:
        planet.gravity = body["gravity"]
    if "population" in body:
        planet.population = body["population"]
    if "terrain" in body:
        planet.terrain = body["terrain"]

    db.session.commit()
    return jsonify("All good, updated!"), 200

@app.route('/delete_planet/<int:id>', methods=['DELETE'])
def del_planet(id):

    # recibir info del request
    planet = Planet.query.get(id)
    if planet is None:
        raise APIException('Planet not found', status_code=404)

    db.session.delete(planet)
    db.session.commit()

    return jsonify("All good, deleted"), 200


############## Endpoints para characters ##############
@app.route('/characters', methods=['GET'])
def get_characters():
    # get all the todos
    character = Character.query.all()

    # map the results and your list of todos  inside of the all_todos variable
    results = list(map(lambda x: x.serialize(), character))

    return jsonify(results), 200

# Obtiene un character especifico
@app.route('/character/<int:id>', methods=['GET'])
def get_character(id):

    character = Character.query.get(id)
    if character is None:
        raise APIException('Character not found', status_code=404)

    return jsonify(character.serialize()), 200


@app.route('/add_character', methods=['POST'])
def add_character():

    # recibir info del request
    request_body = request.get_json()
    print(request_body)

    new_character = Character(name=request_body["name"], birth_year=request_body["birth_year"], height=request_body["height"], mass=request_body["mass"],
        hair_color=request_body["hair_color"], eye_color=request_body["eye_color"], gender=request_body["gender"], planet_id=request_body["planet_id"])
    
    db.session.add(new_character)
    db.session.commit()

    return jsonify("All good, added: ", new_character.serialize()), 200


@app.route('/update_character/<int:id>', methods=['PUT'])
def update_character(id):

    body = request.get_json()
    character = Character.query.get(id)

    if character is None:
        raise APIException('Character not found', status_code=404)
    if body is None:
        raise APIException('Wrong data', status_code=404)

    if "name" in body:
        character.name = body["name"]
    if "birth_year" in body:
        character.birth_year = body["birth_year"]
    if "height" in body:
        character.height = body["height"]
    if "mass" in body:
        character.mass = body["mass"]
    if "hair_color" in body:
        character.hair_color = body["hair_color"]
    if "eye_color" in body:
        character.eye_color = body["eye_color"]
    if "gender" in body:
        character.gender = body["gender"]
    if "planet_id" in body:
        character.planet_id = body["planet_id"]

    db.session.commit()
    return jsonify("All good, updated!"), 200


@app.route('/delete_character/<int:id>', methods=['DELETE'])
def del_character(id):

    # recibir info del request
    character = Character.query.get(id)
    if character is None:
        raise APIException('Character not found', status_code=404)

    db.session.delete(character)
    db.session.commit()

    return jsonify("All good, deleted"), 200

############## Endpoints para favoritos ##############
@app.route('/favorites', methods=['GET'])
def get_favorites():

    # get all the todos
    favorites = Favorite.query.all()
    

    # map the results and your list of todos  inside of the all_todos variable
    results = list(map(lambda x: x.serialize(), favorites))

    return jsonify(results), 200

# Obtiene un favorito especifico
@app.route('/favorite/<int:id>', methods=['GET'])
def get_favorite(id):

    favorite = Favorite.query.get(id)
    if favorite is None:
        raise APIException('Favorite not found', status_code=404)

    return jsonify(favorite.serialize()), 200

@app.route('/add_favorite', methods=['POST'])
def add_favorite():

    # recibir info del request
    request_body = request.get_json()
    print(request_body)

    new_favorite = Favorite(user_id=request_body["user_id"], planet_id=request_body["planet_id"], character_id=request_body["character_id"])
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify("All good, added"), 200

#Delete un favorito con id
@app.route('/delete_favorite/<int:id>', methods=['DELETE'])
def del_favorite(id):

    # recibir info del request
    favorite = Favorite.query.get(id)
    if favorite is None:
        raise APIException('Favorite not found', status_code=404)

    db.session.delete(favorite)
    db.session.commit()

    return jsonify("All good, deleted"), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
