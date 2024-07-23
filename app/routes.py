from flask import Blueprint, jsonify, request
from Shopifybackend.app.app import db
from app.models import User
from flask_jwt_extended import create_access_token

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify(message="Welcome to E-Com Backend!")

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return jsonify({}), 200  

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first() is not None:
        return jsonify(message='Email already registered'), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify(message='User registered successfully'), 201

@auth.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200  

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify(message='Invalid credentials'), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200
