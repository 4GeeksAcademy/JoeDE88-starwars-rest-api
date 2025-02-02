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
from models import db, Users,Favorites,Films,Planets,People,FavoritesType
from random import randint
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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

                                            #GET,POST & DELETE USER 
@app.route('/users', methods=['GET'])
def get_users():
    users_list = Users.query.all()
    response_body = {
        "content": users_list
    }

    return jsonify(response_body), 200

@app.route('/users/<int:user_id>',methods=['GET'])
def get_user(user_id):
    user = Users.query.get(user_id)
    response_body = {
        "content": user
    }
    return jsonify(response_body),200


@app.route('/users', methods=['POST'])
def post_user():
    data = request.get_json(force=True)
    required_fields = {"email", "username","firstname","password"}
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": "Missing required fields", "missing": missing_fields}), 400
    new_user = Users(
        email=data["email"],
        username=data["username"],
        firstname=data["firstname"],
        lastname=data["lastname"],
        password=data["password"],
        is_active=data["is_active"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user),200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"message":"No user found with the requested user_id"}),400

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}),200


                                            # GET,POST & DELETE FAVORITES
@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorites_list = Favorites.query.all()
    response_body = {
        "content": favorites_list
    }
    return jsonify(response_body), 200

@app.route('/favorites',methods=['POST'])
def post_favorites():
    data = request.get_json(force=True)
    required_fields = {"type","external_id","name"}
    if not all(field in data for field in required_fields):
        return jsonify("error: missing required fields"), 400
    
    user_id = 1

    new_favorite = Favorites(
        user_id=user_id,
        external_id=data["external_id"],
        name=data["name"],
        type_enum=data["type"]
    )

    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite), 200


                                            # GET,POST & DELETE FILMS
@app.route('/films',methods=['GET'])
def get_films():
    films_list = Films.query.all()
    response_body = {
        "content": films_list
    }
    return jsonify(response_body),200

@app.route('/films/<int:film_id>',methods=['GET'])
def get_film(film_id):
    film = Films.query.get(film_id)
    response_body = {
        "content": film
    }
    return jsonify(response_body),200

@app.route('/films',methods=['POST'])
def post_film():
    data = request.get_json(force=True)
    required_fields = {"title","episode","release_date","director","producer"}
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return ({"message":"error","missing fields" : missing_fields}),400

    new_film = Films(
        title=data["title"],
        episode=data["episode"],
        release_date=data["release_date"],
        director=data["director"],
        producer=data["producer"],
    )
    db.session.add(new_film)
    db.session.commit()
    return jsonify(new_film),200

@app.route('/planets',methods=['GET'])
def get_planets():
    planets_list = Planets.query.all()
    response_body = {
        "content": planets_list
    }
    return jsonify(response_body),200

@app.route('/planets/<int:planet_id>',methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    response_body = {
        "content": planet
    }
    return jsonify(response_body),200   

@app.route('/people',methods=['GET'])
def get_people():
    people_list = People.query.all()
    response_body = {
        "content": people_list
    }

    return jsonify(response_body),200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)