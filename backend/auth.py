from flask import request,jsonify,make_response
from flask_restx import Resource,fields,Namespace
from model import User
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required,get_jwt_identity

auth_ns = Namespace("auth",description="Namespace for authentication")
signup_model = auth_ns.model(
    "SignUp",{
        "username": fields.String(),
        "password": fields.String(),
        "email": fields.String(),
    }
)

login_model = auth_ns.model(
    "Login",{
        "username": fields.String(),
        "password": fields.String()
    }
)


@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        data = request.get_json()
        username = data['username']
        db_user = User.query.filter_by(username=data['username']).first()
        if db_user is not None:
            return jsonify({"Message": f"User {username} already exists"})

        new_user = User( 
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password'))
        )
        new_user.save()
        return make_response(jsonify({"Message":"New user created successfully"}),201)

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        db_user = User.query.filter_by(username=username).first()

        if db_user is not None and check_password_hash(db_user.password,password):
            access_token = create_access_token(identity=db_user.username)
            refresh_token = create_refresh_token(identity=db_user.username)

            return make_response(jsonify(
                {
                    "Message":"User login successful",
                    "access_token":access_token,
                    "refresh_token":refresh_token
                }
            ),200)

@auth_ns.route('/refresh')
class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return make_response(jsonify({"access_token": new_access_token}))
