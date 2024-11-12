# Proyecto de Gestión de Vehículos y Marcas

Este es un proyecto basado en Flask para gestionar marcas y vehículos. Incluye funcionalidades de registro de marcas y vehículos, listado, edición, eliminación y consultas relacionadas con estas entidades. El proyecto utiliza SQLAlchemy para la manipulación de bases de datos, Flask-WTF para la validación de formularios, y autenticación mediante JWT.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes requisitos:

- **Python 3.8 o superior**
- **MySQL** (o cualquier otra base de datos compatible con SQLAlchemy)
- **Thunder Client** (opcional, para probar los endpoints de la API)

## Tecnologías Utilizadas

- **Flask**: Framework para aplicaciones web en Python.
- **Flask-WTF**: Extensión de Flask para formularios y validación.
- **SQLAlchemy**: ORM para interactuar con bases de datos.
- **Flask-Migrate**: Manejo de migraciones de bases de datos con SQLAlchemy.
- **flask_jwt_extended**: Para la autenticación JWT (JSON Web Tokens).
- **dotenv**: Manejo de variables de entorno.
- **Werkzeug Security**: Manejo de contraseñas seguras.

## Instalación y Configuración

Sigue los pasos a continuación para configurar el entorno de desarrollo:

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/tu-repositorio.git
   cd tu-repositorio
