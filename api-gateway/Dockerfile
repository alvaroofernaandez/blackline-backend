# Usa una imagen base de Python 3.9
FROM python:3.9

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt
COPY requirements.txt .

# Instala las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos los archivos del contexto de construcción al contenedor
COPY . .

# Expone el puerto 8000 para que el contenedor pueda recibir tráfico
EXPOSE 8000

# Establece el directorio de trabajo específico para la aplicación API Gateway
WORKDIR /app/apigateway/

# Comando para iniciar el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
