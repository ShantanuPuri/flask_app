from . import db
from models.job import Job

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    jobs = db.relationship('Job', backref='employee', lazy=True)

    def __init__(self, username, password, full_name, email):
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email

    def __repr__(self):
        return f'<Employee {self.username}>'

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}