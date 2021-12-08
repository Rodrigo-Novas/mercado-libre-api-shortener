from database import db
from sqlalchemy.sql import func

# Creamos tablas usuarios y peliculas


class UsuarioMl(db.Model):
    __tablename__ = "usuariosml"
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(70), nullable=False, unique=True)
    clave = db.Column(db.String(100), nullable=False)
    fecha_de_creacion = db.Column(
        db.DateTime(timezone=True), onupdate=func.now())
    cantidad_ingresos = db.Column(db.Integer)

    def __init__(self, usuario, clave, fecha_de_creacion, cantidad_ingresos) -> None:
        self.usuario = usuario
        self.clave = clave
        self.fecha_de_creacion = fecha_de_creacion
        self.cantidad_ingresos = cantidad_ingresos


class Rutas(db.Model):
    __tablename__ = "rutas"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000, convert_unicode=True),
                    nullable=False, unique=True)
    shortUrl = db.Column(db.String(32), nullable=False, unique=True)
    fecha_de_creacion = db.Column(
        db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, url, shortUrl, fecha_de_creacion) -> None:
        self.url = url
        self.shortUrl = shortUrl
        self.fecha_de_creacion = fecha_de_creacion
