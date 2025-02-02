# Use official Python image as base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl nginx && rm -rf /var/lib/apt/lists/*

# Install Node.js (for Tailwind)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@10.9.2 

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

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Algolyzer.wsgi:application"]
