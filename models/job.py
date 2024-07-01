from . import db

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

    def __init__(self, title, employee_id):
        self.title = title
        self.employee_id = employee_id

    def __repr__(self):
        return f'<Job {self.title}>'
    
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}