import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_marshmallow import Marshmallow
from flask_restx import Api, Resource, Namespace

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
ma = Marshmallow(app)

api = Api(app, version='1.0', title='API de Ejemplo',
          description='Documentación de la API para gestionar usuarios y vehículos')

# Definición de namespaces
usuarios_ns = Namespace('usuarios', description='Operaciones relacionadas con los usuarios')
vehiculos_ns = Namespace('vehiculos', description='Operaciones relacionadas con los vehículos')
marcas_ns = Namespace('marcas', description='Operaciones relacionadas con las marcas')
tipos_ns = Namespace('tipos', description='Operaciones relacionadas con los tipos de vehículos')

# Agregar los namespaces a la API
api.add_namespace(usuarios_ns)
api.add_namespace(vehiculos_ns)
api.add_namespace(marcas_ns)
api.add_namespace(tipos_ns)

from models import User, Marca, Tipo, Vehiculo  # Asegúrate de tener estos modelos definidos.

from View import register_db
register_db(app)

# Rutas para usuarios
@usuarios_ns.route('/')
class UsuarioResource(Resource):
    @usuarios_ns.doc('obtener_usuarios')
    def get(self):
        """Obtiene una lista de usuarios"""
        usuarios = User.query.all()
        return {'usuarios': [usuario.to_dict() for usuario in usuarios]}

    @usuarios_ns.doc('crear_usuario')
    def post(self):
        """Crea un nuevo usuario"""
        # Lógica para crear un usuario
        return {'mensaje': 'Usuario creado'}

# Rutas para vehículos
@vehiculos_ns.route('/')
class VehiculoResource(Resource):
    @vehiculos_ns.doc('obtener_vehiculos')
    def get(self):
        """Obtiene una lista de vehículos"""
        vehiculos = Vehiculo.query.all()
        return {'vehiculos': [vehiculo.to_dict() for vehiculo in vehiculos]}

    @vehiculos_ns.doc('crear_vehiculo')
    @jwt_required()
    def post(self):
        """Crea un nuevo vehículo"""
        current_user = get_jwt_identity()
        # Validar que el usuario sea administrador
        if not User.query.get(current_user).is_admin:
            return {'mensaje': 'Acceso denegado. Solo administradores pueden crear vehículos.'}, 403
        
        data = request.get_json()
        nuevo_vehiculo = Vehiculo(
            modelo=data['modelo'],
            anio_fabricacion=data['anio_fabricacion'],
            precio=data['precio'],
            marca_id=data['marca_id'],
            tipo_id=data['tipo_id']
        )
        db.session.add(nuevo_vehiculo)
        db.session.commit()
        return nuevo_vehiculo.to_dict(), 201  # Usar el método to_dict() del objeto nuevo

# Rutas para marcas
@marcas_ns.route('/')
class MarcaResource(Resource):
    @marcas_ns.doc('obtener_marcas')
    def get(self):
        """Obtiene una lista de marcas"""
        marcas = Marca.query.all()
        return {'marcas': [marca.to_dict() for marca in marcas]}

    @marcas_ns.doc('crear_marca')
    @jwt_required()
    def post(self):
        """Crea una nueva marca"""
        current_user = get_jwt_identity()
        # Validar que el usuario sea administrador
        if not User.query.get(current_user).is_admin:
            return {'mensaje': 'Acceso denegado. Solo administradores pueden crear marcas.'}, 403
        
        data = request.get_json()
        nueva_marca = Marca(nombre=data['nombre'])
        db.session.add(nueva_marca)
        db.session.commit()
        return nueva_marca.to_dict(), 201  # Usar el método to_dict() del objeto nuevo

# Rutas para tipos
@tipos_ns.route('/')
class TipoResource(Resource):
    @tipos_ns.doc('obtener_tipos')
    def get(self):
        """Obtiene una lista de tipos"""
        tipos = Tipo.query.all()
        return {'tipos': [tipo.to_dict() for tipo in tipos]}

    @tipos_ns.doc('crear_tipo')
    @jwt_required()
    def post(self):
        """Crea un nuevo tipo"""
        current_user = get_jwt_identity()
        # Validar que el usuario sea administrador
        if not User.query.get(current_user).is_admin:
            return {'mensaje': 'Acceso denegado. Solo administradores pueden crear tipos.'}, 403
        
        data = request.get_json()
        nuevo_tipo = Tipo(nombre=data['nombre'])  # Asegúrate de que el modelo Tipo tenga el campo 'nombre'
        db.session.add(nuevo_tipo)
        db.session.commit()
        return nuevo_tipo.to_dict(), 201  # Usar el método to_dict() del objeto nuevo

if __name__ == '__main__':
    app.run()
