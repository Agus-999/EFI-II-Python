from flask import Blueprint, request, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from app import db
from models import Vehiculo, Tipo, Marca, User

from schemas import VehiculosSchemas, TipoSchemas, MarcaSchemas

vehiculo_db = Blueprint('vehiculos',__name__)

@vehiculo_db.route('/marcas', methods=['GET', 'POST'])
@jwt_required()
def Marcas():
    additional_data = get_jwt()
    administrador = additional_data.get("administrador")

    if request.method == 'POST':
        if administrador:
            data = request.get_json()
            schema = MarcaSchemas()
            errors = schema.validate(data)

            if errors:
                return make_response(jsonify(errors))

            nueva_marca = Marca(nombre=data.get('nombre'))
            db.session.add(nueva_marca)
            db.session.commit()

            return jsonify(MarcaSchemas().dump(nueva_marca))
        else:
            return jsonify({"Mensaje": "Solo el admin puede crear marcas nuevas"})

    marcas = Marca.query.all()
    return jsonify(MarcaSchemas(many=True).dump(marcas))

@vehiculo_db.route('/tipos', methods=['GET', 'POST'])
@jwt_required()
def Tipos():

    # Obtener datos adicionales del JWT
    additional_data = get_jwt()
    administrador = additional_data.get("administrador")

    if request.method == 'POST':
        # Verificar si el usuario es administrador
        if administrador:
            data = request.get_json()
            schema = TipoSchemas()
            errors = schema.validate(data)

            # Validar datos de entrada
            if errors:
                return make_response(jsonify(errors))

            # Crear nueva marca
            nuevo_tipo = Tipo(nombre=data.get('nombre'))
            db.session.add(nuevo_tipo)
            db.session.commit()

            return TipoSchemas().dump(nuevo_tipo)
        else:
            # Mensaje de acceso denegado si no es administrador
            return jsonify({"Mensaje": "Solo el admin puede crear tipos nuevos"})

    return TipoSchemas().dump(
        Tipo.query.all(), 
        many=True
    )

@vehiculo_db.route('/vehiculos', methods=['GET', 'POST'])
@jwt_required()
def vehiculos():

    additional_data = get_jwt()
    administrador = additional_data.get("administrador")

    if request.method == 'POST':
        
        if administrador:
            
            data = request.get_json()
            schema = VehiculosSchemas()
            errors = schema.validate(data)
            if errors:
                return make_response(jsonify(errors))

            nuevo_vehiculo = Vehiculo(
                modelo = data.get('modelo'),
                anio_fabricacion = data.get('anio_fabricacion'),
                precio = data.get('precio'),
                marca_id = data.get('marca_id'),
                tipo_id = data.get('tipo_id')
            )
            db.session.add(nuevo_vehiculo)
            db.session.commit()
            return VehiculosSchemas().dump(nuevo_vehiculo)
        else:
            return jsonify({"Mensaje": "Solo el admin puede crear vehiculos nuevos"})

    vehiculos = Vehiculo.query.all()
    return VehiculosSchemas().dump(vehiculos, many=True)


@vehiculo_db.route('/vehiculos/<int:id>', methods=['PUT', 'DELETE'])
@jwt_required()
def gestionar_vehiculo(id):
    additional_data = get_jwt()
    administrador = additional_data.get("administrador")

    # Verificar que el usuario sea administrador
    if not administrador:
        return jsonify({"Mensaje": "Solo el admin puede modificar o eliminar vehiculos"})

    vehiculo = Vehiculo.query.get(id)
    if not vehiculo:
        return jsonify({"Mensaje": "Vehículo no encontrado"}), 404

    if request.method == 'PUT':
        # Actualización de un vehículo
        data = request.get_json()
        vehiculo.modelo = data.get('modelo', vehiculo.modelo)
        vehiculo.anio_fabricacion = data.get('anio_fabricacion', vehiculo.anio_fabricacion)
        vehiculo.precio = data.get('precio', vehiculo.precio)
        vehiculo.marca_id = data.get('marca_id', vehiculo.marca_id)
        vehiculo.tipo_id = data.get('tipo_id', vehiculo.tipo_id)

        db.session.commit()

        return jsonify(VehiculosSchemas().dump(vehiculo))

    elif request.method == 'DELETE':
        # Eliminación de un vehículo
        db.session.delete(vehiculo)
        db.session.commit()

        return jsonify({"Mensaje": "Vehículo eliminado exitosamente"})
