# Base image
FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Change into the Django project directory
WORKDIR /app/MyDiary

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port Django/Gunicorn will run on
EXPOSE 8000

# Start Gunicorn server
CMD ["gunicorn", "--chdir", ".", "MyDiary.wsgi:application", "--bind", "0.0.0.0:8000"]
