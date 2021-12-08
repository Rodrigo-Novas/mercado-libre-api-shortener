from flask_marshmallow import Marshmallow

ma = Marshmallow()

# esquema de usuario


class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ("id", "usuario", "clave",
                  "fecha_de_creacion", "cantidad_ingresos")


class RutasSchema(ma.Schema):
    class Meta:
        fields = ("id", "url", "shortUrl", "fecha_de_creacion")


ruta_schema = RutasSchema()
rutas_schema = RutasSchema(many=True)
usuarios_schema = UsuarioSchema(many=True)
