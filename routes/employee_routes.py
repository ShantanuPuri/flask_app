from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import *

employee_routes = Blueprint('employee_routes', __name__)
bcrypt = Bcrypt()

@employee_routes.route('/employees', methods=['POST'])
@jwt_required()
def create_employee():
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
        new_employee = Employee(username=username, password=hashed_password, full_name=full_name, email=email)
        # new_user = Employee(username=username, password=password)

        db.session.add(new_employee)
        db.session.commit()

        return jsonify({"message": "New employee added."}), 201
    else:
        return jsonify({"message": "Request must be JSON."}), 415

@employee_routes.route('/employees/<int:id>', methods=['GET'])
@jwt_required()
def get_employee(id):
    from models.employee import Employee
    employee = Employee.query.get(id)
    if employee:
        return jsonify(employee.as_dict()), 200
    return jsonify({"message": "Employee not found."}), 404

@employee_routes.route('/employees/page/<int:page_no>', methods=['GET'])
@jwt_required()
def get_employees(page_no):
    from models.employee import Employee
    page = request.args.get('page', page_no, type=int)
    per_page = request.args.get('per_page', 1, type=int)
    employees = Employee.query.paginate(page=page, per_page=per_page, error_out=False)
    if not employees:
        return jsonify({'message': 'No employees found.'}), 404
    employee_list = [employee.as_dict() for employee in employees]
    return jsonify({'employees': employee_list, 'total_pages': employees.pages, 'current_page': employees.page, 'total_employees': employees.total}), 200

@employee_routes.route('/employees/<int:id>', methods=['POST'])
@jwt_required()
def update_employeee(id):
    from models import db
    from models.employee import Employee
    employee = Employee.query.get(id)
    if employee:
        data = request.get_json()
        employee.username = data.get('username', employee.username)
        password = data.get('password')
        if password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            employee.password = hashed_password
        employee.full_name = data.get('full_name', employee.full_name)
        employee.email = data.get('email', employee.email)
        try:
            db.session.commit()
            return jsonify({"message": "Employee updated successfully."}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Error occurred while updating employee.", "error": str(e)}), 500
    return jsonify({"message": "Employee not found."}), 404

@employee_routes.route('/employees/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_employee(id):
    from models import db
    from models.employee import Employee
    employee = Employee.query.get(id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({"message": "Employee deleted successfully."}), 200
    return jsonify({"message": "Employee not found."}), 404