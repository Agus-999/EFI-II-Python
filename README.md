Documentación de la API - Proyecto de Gestión de Usuarios y Vehículos
Este proyecto es una API RESTful desarrollada en Flask para gestionar usuarios y vehículos. Utiliza varias bibliotecas y herramientas para la autenticación, validación de datos, y manejo de la base de datos. A continuación, se describen las funcionalidades, rutas, y estructura general de la aplicación.

Estructura del Proyecto
El proyecto se divide en las siguientes secciones principales:

app.py: Contiene la configuración principal de la aplicación, inicializa las extensiones y define las rutas para los recursos de la API (usuarios, vehículos, marcas, y tipos).
forms.py: Define un formulario de registro utilizando Flask-WTF.
models.py: Define los modelos de la base de datos usando SQLAlchemy (Marca, Tipo, Vehículo, y Usuario).
schemas.py: Crea esquemas de validación y serialización con Marshmallow.
views/: Contiene las vistas (blueprints) que manejan las rutas de autenticación y gestión de vehículos.
Configuración de la Aplicación
La configuración de la aplicación se maneja mediante variables de entorno:

SQLALCHEMY_DATABASE_URI: URI de la base de datos, obtenida de un archivo .env.
SECRET_KEY: Clave secreta para la autenticación.
Instalación
Clonar el repositorio:
bash
Copiar código
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>
Crear un entorno virtual:
bash
Copiar código
python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows
Instalar las dependencias:
bash
Copiar código
pip install -r requirements.txt
Configurar el entorno:
Crear un archivo .env en el directorio raíz con las siguientes variables:
makefile
Copiar código
SQLALCHEMY_DATABASE_URI=tu_URI_de_base_de_datos
SECRET_KEY=tu_clave_secreta
Modelos de Base de Datos
User: Modelo para los usuarios con atributos username, password_hash y is_admin.
Marca: Modelo para las marcas de vehículos.
Tipo: Modelo para los tipos de vehículos.
Vehículo: Modelo para los vehículos, que incluye relaciones con Marca y Tipo.
Rutas de la API
Autenticación
POST /login: Genera un token de acceso JWT para la autenticación de usuarios.
GET /users: Lista todos los usuarios (oculta información sensible si el usuario no es administrador).
POST /users: Crea un nuevo usuario (solo accesible para administradores).
Gestión de Vehículos
GET /vehiculos: Lista todos los vehículos.
POST /vehiculos: Crea un nuevo vehículo (solo administradores).
GET /marcas: Lista todas las marcas.
POST /marcas: Crea una nueva marca (solo administradores).
GET /tipos: Lista todos los tipos de vehículos.
POST /tipos: Crea un nuevo tipo (solo administradores).
Seguridad
La API utiliza JWT (JSON Web Token) para la autenticación y protección de rutas. Las rutas sensibles requieren un token de acceso válido, y solo los administradores pueden realizar ciertas acciones, como crear nuevos usuarios o vehículos.

Validación y Serialización
Se utiliza Flask-Marshmallow y WTForms para validar y serializar los datos de las solicitudes. Se aseguran de que los datos sean válidos antes de procesarlos y almacenarlos en la base de datos.

Ejecución de la Aplicación
Ejecutar la aplicación:

bash
Copiar código
flask run
La aplicación estará disponible en http://localhost:5000.

Realizar migraciones de base de datos:

bash
Copiar código
flask db init
flask db migrate -m "mensaje de migración"
flask db upgrade
Dependencias Principales
Flask: Framework principal de la aplicación.
Flask-SQLAlchemy: Extensión para la gestión de la base de datos.
Flask-Migrate: Manejo de migraciones de la base de datos.
Flask-JWT-Extended: Autenticación mediante tokens JWT.
Flask-WTF: Manejo de formularios con validación.
Marshmallow: Serialización y validación de datos.
Pruebas y Uso
Se recomienda usar herramientas como Postman o Thunder Client para probar las rutas de la API. Asegúrate de enviar el token de autenticación en las solicitudes protegidas.

Contribución
Si deseas contribuir al proyecto, por favor sigue las pautas de contribución que se encuentran en el archivo CONTRIBUTING.md.
