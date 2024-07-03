flask_app Objective:
* Create a Flask application with user authentication (using JWT), CRUD operations.
* Create Employee and Job models.
* Ensure a one-to-many relationship (Employee can have many Jobs)
* Implement pagination for the GET endpoint.
* Use SQLAlchemy for ORM (Object Relational Mapping).
* Store data in a MySQL database.
* Containerize the application using Docker. 
* Deploy the application on AWS or Azure (I chose AWS EC2).

Code Details:
* app.py - sets up the flask app, creates db tables, registers route blueprints, and runs the flask app.

* models/__init__.py - imports SQLAlchemy and creates the db.
* models/employee.py - creates the Employee class.
* models/job.py - creates the Job class.
  
* routes/__init__.py - imports Blueprint and creates the auth blueprint.
* routes/auth.py - creates endpoints for user registration, login, logout, and get user.
* routes/employee_routes.py - creates endpoints to create, read, update, delete employees. 
* routes/job_routes.py - creates endpoints to create, read, update, delete jobs.

* Dockerfile - instructions to create the Docker image for the flask container.
* mysql/Dockerfile.mysql - instructions to create the Docker image for the mysql container.
* mysql/my.cnf - configuration file for MySQL.
* docker-compose.yml - defines the configuration of both Docker containers.
* .dockerignore - specifies files and directories to be excluded when building Docker images.
* requirements.txt - specifies dependencies required for the project to run.

Testing the flask app using CURL commands:
NOTE #1: for each of the commands below, please replace the URL with the URL currently in use by the flask app.
NOTE #2: an access token will be required for most endpoints, please obtain one by using the login endpoint. Then, use this access token to replace <your_access_token>
1. Authentication Endpoints:
* Register new user - curl -X POST http://0.0.0.0:5000/register -H 'Content-Type: application/json' -d '{"username": "new_user", "password": "new_password", "full_name": "New User", "email": "new_user@example.com"}'
* User login - curl -X POST http://0.0.0.0:5000/login -H 'Content-Type: application/json' -d '{"username": "new_user", "password": "new_password"}'
* User logout - curl -X POST http://0.0.0.0:5000/logout -H "Authorization: Bearer <your_access_token>"
* Get user - curl -X GET http://0.0.0.0:5000/protected -H "Authorization: Bearer <your_access_token>"

2. Employee Endpoints:
* Create new employee - curl -X POST http://0.0.0.0:5000/employees -H 'Content-Type: application/json' -d '{"username": "new_user", "password": "new_password", "full_name": "New User", "email": "new_user@example.com"}' -H "Authorization: Bearer <your_access_token>"
* Get employee (replace <int:id> with desired employee_id) - curl -X GET http://0.0.0.0:5000/employees/<int:id> -H "Authorization: Bearer <your_access_token>"
* Get all employees (replace <int:id> with desired page no.) - curl -X GET http://0.0.0.0:5000/employees/page/<int:id> -H "Authorization: Bearer <your_access_token>"
* Update employee (replace <int:id> with desired employee_id) - curl -X POST http://0.0.0.0:5000/employees/<int:id> -H 'Content-Type: application/json' -d '{"username": "new_user", "password": "new_password", "full_name": "New User", "email": "new_user@example.com"}' -H "Authorization: Bearer <your_access_token>"
* Delete employee (replace <int:id> with desired employee_id) - curl -X DELETE http://0.0.0.0:5000/employees/<int:id> -H "Authorization: Bearer <your_access_token>"

3. Job Endpoints:
* Create new job - curl -X POST http://0.0.0.0:5000/jobs -H 'Content-Type: application/json' -d '{"title": "HR", "employee_id": "1"}' -H "Authorization: Bearer <your_access_token>"
* Get job (replace <int:id> with desired job_id) - curl -X GET http://0.0.0.0:5000/jobs/<int:id> -H "Authorization: Bearer <your_access_token>"
* Get all jobs (replace <int:id> with desired page no.) - curl -X GET http://0.0.0.0:5000/jobs/page/<int:id> -H "Authorization: Bearer <your_access_token>"
* Update job (replace <int:id> with desired job_id) - curl -X POST http://0.0.0.0:5000/jobs/<int:id> -H 'Content-Type: application/json' -d '{"title": "HR", "employee_id": "1"}' -H "Authorization: Bearer <your_access_token>"
* Delete job (replace <int:id> with desired job_id) - curl -X DELETE http://0.0.0.0:5000/jobs/<int:id> -H "Authorization: Bearer <your_access_token>"
