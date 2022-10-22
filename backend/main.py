from distutils import core
import re
from turtle import title
from flask import Flask,request,jsonify
from flask_restx import Api,Resource,fields
from model import User
from recipe import recipe_ns
from auth import auth_ns
from model import Recipe
from exts import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app)
    db.init_app(app)
    api = Api(app,doc='/docs')
    migrate = Migrate(app=app,db=db)
    JWTManager(app)
    api.add_namespace(auth_ns)
    api.add_namespace(recipe_ns)


    @app.shell_context_processor
    def make_shell_context():
        return {
            "db":db,
            "Recipe":Recipe,
            "User" : User
        }

    return app

