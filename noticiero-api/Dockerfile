FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002

WORKDIR /app/noticiero/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]
