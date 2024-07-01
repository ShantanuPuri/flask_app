from flask import Blueprint, request, jsonify
from flask_jwt_extended import *

job_routes = Blueprint('job_routes', __name__)

@job_routes.route('/jobs', methods=['POST'])
@jwt_required()
def create_job():
    from models import db
    from models.job import Job
    if request.is_json:
        data = request.get_json()
        title = data.get('title')
        employee_id = data.get('employee_id')
        
        new_job = Job(title=title, employee_id=employee_id)

        db.session.add(new_job)
        db.session.commit()

        return jsonify({"message": "New job added."}), 201
    else:
        return jsonify({"message": "Request must be JSON."}), 415

@job_routes.route('/jobs/<int:id>', methods=['GET'])
@jwt_required()
def get_job(id):
    from models.job import Job
    job = Job.query.get(id)
    if job:
        return jsonify(job.as_dict()), 200
    return jsonify({"message": "Job not found."}), 404

@job_routes.route('/jobs/page/<int:page_no>', methods=['GET'])
@jwt_required()
def get_jobs(page_no):
    from models.job import Job
    page = request.args.get('page', page_no, type=int)
    per_page = request.args.get('per_page', 1, type=int)
    jobs = Job.query.paginate(page=page, per_page=per_page, error_out=False)
    if not jobs:
        return jsonify({'message': 'No jobs found.'}), 404
    job_list = [job.as_dict() for job in jobs]
    return jsonify({'jobs': job_list, 'total_pages': jobs.pages, 'current_page': jobs.page, 'total_employees': jobs.total}), 200

@job_routes.route('/jobs/<int:id>', methods=['POST'])
@jwt_required()
def update_job(id):
    from models import db
    from models.job import Job
    job = Job.query.get(id)
    if job:
        data = request.get_json()
        job.title = data.get('title', job.title)
        job.employee_id = data.get('employee_id', job.employee_id)
        try:
            db.session.commit()
            return jsonify({"message": "Job updated successfully."}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Error occurred while updating job.", "error": str(e)}), 500
    return jsonify({"message": "Job not found."}), 404

@job_routes.route('/jobs/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_job(id):
    from models import db
    from models.job import Job
    job = Job.query.get(id)
    if job:
        db.session.delete(job)
        db.session.commit()
        return jsonify({"message": "Job deleted successfully."}), 200
    return jsonify({"message": "Job not found."}), 404