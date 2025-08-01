# Use Python 3.11 slim image
FROM python:3.11-slim

# ─── Environment ────────────────────────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ─── Work dir ──────────────────────────────────────────────────────────────────
WORKDIR /app

# ─── System deps ───────────────────────────────────────────────────────────────
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
         postgresql-client \
         build-essential \
         libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ─── Python deps ───────────────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─── Copy code ─────────────────────────────────────────────────────────────────
COPY . .

# ─── Prepare static & media folders ────────────────────────────────────────────
# Create the folders and make them world-writable so that collectstatic can write into them
RUN mkdir -p /app/staticfiles /app/media \
    && chmod -R 777 /app/staticfiles /app/media

# ─── Non-root user ──────────────────────────────────────────────────────────────
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app

USER appuser

# ─── Ports & Startup ───────────────────────────────────────────────────────────
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
