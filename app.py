from flask import Flask
from flask_jwt_extended import *
from flask_bcrypt import Bcrypt
from models import db
from sqlalchemy.exc import OperationalError
from models.employee import Employee
from models.job import Job
import os  

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql+pymysql://root:root_password@mysql_db/flask_app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret key do not share'

db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return "Hello, Flask_App2!"

with app.app_context():
    try:
        db.create_all()
    except OperationalError as e:
        if 'already exists' in str(e):
            print("Tables already exist, skipping creation.")
    except Exception as e:
        print(f"Error creating database tables: {str(e)}")

from routes.auth import auth
app.register_blueprint(auth, url_prefix='/') 

from routes.job_routes import job_routes
app.register_blueprint(job_routes, url_prefix='/') 

from routes.employee_routes import employee_routes
app.register_blueprint(employee_routes, url_prefix='/')  

if __name__ == '__main__':
    app.run()