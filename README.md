# 🖤 Blackline Backend

**Repositorio del backend del Trabajo de Fin de Grado de Álvaro Fernández, Juan Deogracias y Francisco Bermejo.**

Este proyecto representa la capa de servidor de la aplicación **Blackline**, desarrollada como parte del Trabajo de Fin de Grado. La arquitectura se basa en microservicios, cada uno encargado de una funcionalidad específica, y se orquesta mediante contenedores Docker y Kubernetes para garantizar escalabilidad y mantenimiento eficiente.

## 🧱 Estructura del Proyecto

- `api-gateway/`: Puerta de enlace que gestiona las solicitudes entrantes y las distribuye a los microservicios correspondientes.
- `api-principal/`: Microservicio principal que maneja la lógica central de la aplicación.
- `noticiero-api/`: Microservicio encargado de la gestión de noticias y actualizaciones.
- `sorteos-api/`: Microservicio responsable de la gestión de sorteos y concursos.
- `kubernetes/`: Archivos de configuración para el despliegue en un clúster de Kubernetes.
- `docker-compose.yml`: Definición de servicios y redes para el entorno de desarrollo local.
- `init.sql`: Script de inicialización de la base de datos con las estructuras y datos necesarios.

## 🚀 Tecnologías Utilizadas

- **Lenguaje de programación**: Python
- **Frameworks**: Django, DRF
- **Base de datos**: PostgreSQL, MongoDB
- **Contenedorización**: Docker
- **Orquestación**: Kubernetes
- **Control de versiones**: Git

## ⚙️ Requisitos Previos

- [Especificar versión del lenguaje]
- Docker
- Docker Compose
- Kubernetes (opcional, para producción)

## 🛠️ Instalación y Ejecución

1. Clona el repositorio:

   ```bash
   git clone https://github.com/alvaroofernaandez/blackline-backend.git
   cd blackline-backend
   ```
2. Inicia los servicios con Docker Compose:
   
   ```bash
    docker-compose up --build
   ```
3. Accede a la aplicación a través del navegador:
   
    ```bash
    http://localhost:4321
   ```
## 🤝Contribuciones

1. Haz un fork del repositorio.
2. Crea una nueva rama: git checkout -b feature/nueva-funcionalidad
3. Realiza tus cambios y haz commit.
4. Haz push a tu rama.
5. Abre un Pull Request.

## 📬 Contacto

- Álvaro Fernández: [Contacta a Álvaro](https://www.linkedin.com/in/alvaroofernaandez/)
- Juan Deogracias: [Contacta a Juan](https://www.linkedin.com/in/juan-deogracias-moya/)
- Francisco Bermejo: [Contacta a Fran](https://www.linkedin.com/in/francisco-bermejo-melero-250669302/)
