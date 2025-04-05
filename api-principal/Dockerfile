FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

COPY wait-for-mysql.sh /app/principal/
RUN chmod +x wait-for-mysql.sh

WORKDIR /app/usuarios/

CMD ["./wait-for-mysql.sh", "python", "manage.py", "runserver", "0.0.0.0:8001"]
