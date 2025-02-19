FROM python:3.10

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir Flask google-generativeai python-dotenv

COPY . .

EXPOSE 5000

RUN python3 /app/picsort.py

CMD ["python3", "/app/app.py"]
