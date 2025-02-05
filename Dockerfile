# Use Python slim image as base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    bash \
    nodejs \
    npm && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Install specific npm version
RUN npm install -g npm@10.9.2 

# Copy requirements.txt
COPY ./requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Install Node.js dependencies (Tailwind, etc.)
COPY ./package.json /app/
RUN npm install

# Copy project files
COPY . /app/

# Run tailwind build
RUN npm run tw_build

# Change working directory
WORKDIR /app/Algolyzer/

# Migrate database
RUN python manage.py migrate

# Create superuser using env values
RUN python manage.py create_superuser

# Seed the database
RUN python manage.py loaddata data/*

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Use production settings instead of default development settings       
ENV DJANGO_SETTINGS_MODULE=Algolyzer.settings.production

# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-", "Algolyzer.wsgi:application"]
