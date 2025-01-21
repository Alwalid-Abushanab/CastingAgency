from database import setup_db, db
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models.movie import Movie
from models.actor import Actor
from datetime import date
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get("SQLALCHEMY_DATABASE_URI")
        setup_db(app, database_path=database_path)

    with app.app_context():
        db.create_all()

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/movies", methods=["GET"])
    @requires_auth('get:movies')
    def retrieve_movies(jwt):
        movies = Movie.query.order_by(Movie.id).all()

        return jsonify(
            {
                "success": True,
                "movies": [moive.format() for moive in movies],
            }
        )
        
    @app.route("/actors", methods=["GET"])
    @requires_auth('get:actors')
    def retrieve_actors(jwt):
        actors = Actor.query.order_by(Actor.id).all()

        return jsonify(
            {
                "success": True,
                "actors": [actor.format() for actor in actors],
            }
        )
        
    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        movie = Movie.query.get(movie_id)

        if movie is None:
            abort(404)

        try:
            movie.delete()

            return jsonify(
                {
                    "success": True,
                }
            )
        except:
            abort(422)
            
    @app.route("/actors/<int:actor_id>", methods=["DELETE"])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        actor = Actor.query.get(actor_id)

        if actor is None:
            abort(404)

        try:
            actor.delete()

            return jsonify(
                {
                    "success": True,
                }
            )
        except:
            abort(422)
            
    @app.route("/actors", methods=["POST"])
    @requires_auth('post:actor')
    def add_actor(jwt):
        data = request.get_json()

        try:
            new_actor = Actor(name=data["name"], age=data["age"], gender=data["gender"] )
            new_actor.insert()

            return jsonify(
                {
                    "success": True,
                }
            ), 201
        except:
            abort(422)
            
    @app.route("/movies", methods=["POST"])
    @requires_auth('post:movies')
    def add_moive(jwt):
        data = request.get_json()

        try:
            new_movie = Movie(title=data["title"], release_date=data["release_date"])
            new_movie.insert()

            return jsonify(
                {
                    "success": True,
                }
            ), 201
        except:
            abort(422)
            
    @app.route("/actors/<int:actor_id>", methods=["PATCH"])
    @requires_auth('patch:actor')
    def update_actor(jwt, actor_id):
        data = request.get_json()

        try:
            actor = Actor.query.get(actor_id)
            if not actor:
                abort(404)

            if "name" in data:
                actor.name = data["name"]
            if "age" in data:
                actor.age = data["age"]
            if "gender" in data:
                actor.gender = data["gender"]

            actor.update()

            return jsonify({
                "success": True,
            }), 200
        except:
            abort(422)
            
    @app.route("/movies/<int:movie_id>", methods=["PATCH"])
    @requires_auth('patch:movies')
    def update_movie(jwt, movie_id):
        data = request.get_json()

        try:
            movie = Movie.query.get(movie_id)
            if not movie:
                abort(404)

            if "title" in data:
                movie.title = data["title"]
            if "release_date" in data:
                movie.release_date = data["release_date"]

            movie.update()

            return jsonify({
                "success": True,
            }), 200
        except:
            abort(422)
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400
        
    @app.errorhandler(Exception)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500
    
    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code


    return app
