FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8003

WORKDIR /app/sorteos/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8003"]
