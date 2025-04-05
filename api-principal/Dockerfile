FROM python:3.9

RUN apt-get update && apt-get install -y default-mysql-client

WORKDIR /app/usuarios

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY wait-for-mysql.sh /app/
RUN chmod +x /app/wait-for-mysql.sh

EXPOSE 8001

CMD ["sh", "-c", "/app/wait-for-mysql.sh && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8001"]
