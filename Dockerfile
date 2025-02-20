FROM python:3.10

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir Flask google-generativeai

COPY . .

EXPOSE 5000

CMD ["python3", "/app/app.py"]
