# Use a Python base image
FROM python:3.8-slim

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       wget \
       pkg-config \
       gcc \
       python3-dev \
       libmariadb-dev-compat \
       default-libmysqlclient-dev \
       musl-dev \
       mariadb-client \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Expose port 5000
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apt-get update && apt-get install -y wget \
    && wget -O /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x /usr/local/bin/wait-for-it.sh

# Run Gunicorn server
CMD ["wait-for-it.sh", "mysql-container:3306", "--", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
