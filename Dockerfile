# ✅ Base image — required!
FROM python:3.11-slim

# ✅ Avoid Python bytecode & buffer issues
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ✅ Set working directory
WORKDIR /app

# ✅ System dependencies (for psycopg2, etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ✅ Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy entire project
COPY . .

# ✅ Set static files destination in settings.py:
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Then collect static files
RUN python manage.py collectstatic --noinput

# ✅ Expose port
EXPOSE 8000

# ✅ Run Gunicorn from correct dir
CMD ["gunicorn", "--chdir", "MyDiary", "MyDiary.wsgi:application", "--bind", "0.0.0.0:8000"]
