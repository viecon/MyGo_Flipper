FROM python:3.12.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--access-logfile -", "--error-logfile -"]

