from datetime import timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import check_password_hash
from models import User
from app import db
from schemas import UserSchemas, NoAdminSchemas
from marshmallow import ValidationError

auth_db = Blueprint('auth', __name__)

@auth_db.route("/login", methods=['POST'])
def login():
    data = request.authorization
    if not data or not data.username or not data.password:
        return jsonify({"Mensaje": "Se requiere nombre de usuario y contraseña"})

    username = data.username
    password = data.password

    usuario = User.query.filter_by(username=username).first()
    
    if usuario and (usuario.password_hash == password or check_password_hash(usuario.password_hash, password)):
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=60),
            additional_claims={"administrador": usuario.is_admin}
        )
        return jsonify({'Token': f'Bearer {access_token}'})

    return jsonify({"Mensaje": "El usuario y la contraseña no coinciden"})

@auth_db.route('/users', methods=['GET', 'POST'])
@jwt_required()
def users():
    additional_data = get_jwt()
    administrador = additional_data.get("administrador")
    
    if request.method == 'POST':
        if administrador:
            data = request.get_json()
            username = data.get('usuario')
            password = data.get('contraseña')

            if not username or not password:
                return jsonify({"mensaje": "Se requieren nombre de usuario y contraseña"})

            # Validar el username usando UserSchemas
            schema = UserSchemas()
            try:
                # Intentar validar el username
                schema.load({"username": username}, partial=("password_hash", "is_admin"))
                
                nuevo_usuario = User(
                    username=username,
                    password_hash=password,
                    is_admin=False
                )
                db.session.add(nuevo_usuario)
                db.session.commit()
                return jsonify({
                    "mensaje": "Usuario creado correctamente",
                    "Usuario": {"username": nuevo_usuario.username}
                })
            except ValidationError:
                return jsonify({"mensaje": "El nombre de usuario ya existe"})
        else:
            return jsonify({"mensaje": "Solo el admin puede crear nuevos usuarios"})

    usuarios = User.query.all()
    if administrador:
        return UserSchemas().dump(obj=usuarios, many=True)
    else:
        return NoAdminSchemas().dump(obj=usuarios, many=True)
