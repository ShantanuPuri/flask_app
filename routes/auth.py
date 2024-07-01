from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import *

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route('/register', methods=['POST'])
def register():
    from models import db
    from models.employee import Employee
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        full_name = data.get('full_name')
        email = data.get('email')

        if Employee.query.filter_by(username=username).first():
            return jsonify({"message": "Username already exists."}), 400
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = Employee(username=username, password=hashed_password, full_name=full_name, email=email)
        # new_user = Employee(username=username, password=password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "New user added."}), 201
    else:
        return jsonify({"message": "Request must be JSON."}), 415

@auth.route('/login', methods=['POST'])
def login():
    from models.employee import Employee
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = Employee.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"message": "Invalid username or password."}), 401   
    else:
        return jsonify({"message": "Request must be JSON."}), 415

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    current_user = get_jwt_identity()
    return jsonify({"message": "User has been logged out."}), 200

@auth.route('/protected', methods=['GET'])
@jwt_required() 
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200