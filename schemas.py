from app import ma, db
from models import User, Tipo, Marca, Vehiculo
from marshmallow import validates, ValidationError, fields
from datetime import datetime

class UserSchemas(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("id", "username", "password_hash", "is_admin")

    @validates("username")
    def validate_username(self, value):
        # Verificar si el usuario ya existe en la base de datos
        if User.query.filter_by(username=value).first():
            raise ValidationError("El nombre de usuario ya existe")

class NoAdminSchemas(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("username",)  # Asegúrate de que esto sea una tupla añadiendo la coma

class TipoSchemas(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tipo
        fields = ("nombre",)  # Asegúrate de añadir una coma para que sea una tupla

class MarcaSchemas(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Marca
        fields = ("nombre",)  # Asegúrate de añadir una coma para que sea una tupla

class VehiculosSchemas(ma.SQLAlchemyAutoSchema):
    marca = fields.Nested(MarcaSchemas, only=("id", "nombre"))
    tipo = fields.Nested(TipoSchemas, only=("id", "nombre"))

    class Meta:
        model = Vehiculo
        fields = ("id", "modelo", "anio_fabricacion", "precio", "marca_id", "tipo_id")
    
    @validates('anio_fabricacion')
    def validate_anio_fabricacion(self, value):
        current_year = datetime.now().year
        if value < current_year:  # Cambiado de > a <
            raise ValidationError("El año de fabricación debe ser el año actual o posterior.")
