from app import db

class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __str__(self) -> str:
        return self.nombre
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
        }

class Tipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __str__(self) -> str:
        return f"Tipo {self.nombre}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
        }

class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(50), nullable=False)
    anio_fabricacion = db.Column(db.Integer)
    precio = db.Column(db.Integer)

    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=False)  # Corrección ForeignKey
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo.id'), nullable=False)  # Corrección ForeignKey

    marca = db.relationship('Marca', backref=db.backref('vehiculos', lazy=True))
    tipo = db.relationship('Tipo', backref=db.backref('vehiculos', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'modelo': self.modelo,
            'anio_fabricacion': self.anio_fabricacion,
            'precio': self.precio,
            'marca_id': self.marca_id,
            'tipo_id': self.tipo_id,
            'marca': self.marca.nombre if self.marca else None,  # Nombre de la marca
            'tipo': self.tipo.nombre if self.tipo else None,  # Nombre del tipo
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean)  # Alineado con el código de migración


    def to_dict(self):
        return dict(
            username = self.username,
            password = self.password_hash,
        )