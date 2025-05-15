FROM python:3.9

RUN apt-get update && apt-get install -y default-mysql-client

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY usuarios ./usuarios

COPY wait-for-mysql.sh /app/
RUN chmod +x /app/wait-for-mysql.sh

EXPOSE 8001

CMD ["sh", "-c", "sleep 30 && python usuarios/manage.py makemigrations && python usuarios/manage.py migrate && python usuarios/manage.py runserver 0.0.0.0:8001"]
