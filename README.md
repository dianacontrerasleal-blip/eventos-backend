<h1 align="center">🎫 Sistema de Gestión de Eventos y Taquilla</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white" alt="Python 3.11">
  <img src="https://img.shields.io/badge/FastAPI-005571?logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" alt="Docker">
</p>

## 📖 Descripción del Proyecto
Este repositorio contiene el backend (API REST) robusto para la administración de eventos, recintos y venta de boletería digital. El sistema enlaza la gestión de usuarios asistentes con un inventario de eventos, asegurando la integridad de datos y controlando matemáticamente los límites de aforo.

## 🚀 Características Principales
- **CRUD Completo:** Módulo de administración de Usuarios, Eventos y Boletos.
- **Control Estricto de Aforo:** Regla de negocio core que valida en tiempo real la disponibilidad de un recinto antes de emitir y cobrar un boleto, evitando así la sobreventa y bloqueando peticiones maliciosas (HTTP 400).
- **Filtros Dinámicos:** Búsqueda rápida de eventos basada en palabras clave de ubicación (ej. *Auditorio*, *Aula*).
- **Documentación Interactiva:** Interfaz visual Swagger autogenerada para pruebas inmediatas.
- **Despliegue Contenerizado:** Entorno orquestado por Docker Compose con PostgreSQL.

## 🏗️ Estructura del Repositorio
- `app/models.py`: Modelos de la base de datos (SQLAlchemy).
- `app/schemas.py`: Validadores y estructuradores de JSON (Pydantic).
- `app/main.py`: Declaración de endpoints y reglas de negocio.
- `app/database.py`: Enlace a la persistencia en PostgreSQL.
- `alembic/`: Gestión del historial y migraciones de la base de datos.

## ⚙️ Pre-requisitos
Asegúrate de contar con los siguientes programas instalados:
- [Docker](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com/)

## 🛠️ Instrucciones de Ejecución

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/dianacontrerasleal-blip/eventos-backend.git
   cd eventos-backend
   ```

2. **Configurar el entorno**
   Renombra el archivo de ejemplo a su versión definitiva `.env` para que el sistema reconozca las credenciales.
   ```bash
   cp .env.example .env
   ```

3. **Orquestar servicios**
   Levanta la imagen de la API y de PostgreSQL de forma automatizada:
   ```bash
   docker-compose up -d
   ```

4. **Migrar Base de Datos**
   Construye las tablas y sus relaciones ejecutando Alembic dentro del contenedor:
   ```bash
   docker-compose exec web alembic upgrade head
   ```

## 🌐 Pruebas Interactivas
Cuando los contenedores indiquen estar listos, dirígete a la consola de pruebas (Swagger UI) desde tu navegador:
👉 **[http://localhost:8002/docs](http://localhost:8002/docs)**

Esta documentación te permitirá realizar todos los tests de manera gráfica y comprobar el control de aforo por ti mismo.
