# Use official Python image with Alpine as base
FROM python:3.12-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1 

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apk update && \
    apk add --no-cache \
    curl \
    nginx \
    bash \
    nodejs \
    npm && \
    rm -rf /var/cache/apk/*

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

WORKDIR /app/Algolyzer/

# Run tailwind build
RUN npm run tw_build

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Algolyzer.wsgi:application"]
