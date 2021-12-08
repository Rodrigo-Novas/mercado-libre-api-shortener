from flask import Blueprint, request, jsonify, current_app, redirect
from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import create_access_token
from werkzeug.exceptions import abort
from models.model import Rutas, UsuarioMl, db
from schemas.schema import ruta_schema, usuarios_schema, rutas_schema
import bcrypt
from datetime import datetime
from utils.util import Utils
from flask_expects_json import expects_json

blue_print = Blueprint("app", __name__, url_prefix="/api/ML")

# Esquemas

SCHEMA_USUARIOS = {
    "type": "object",
    "properties": {
        "usuario": {"type": "string"},
        "clave": {"type": "string"}
    },
    "required": ["usuario", "clave"]
}

SCHEMA_RUTAS = {
    "type": "object",
    "properties": {
        "url": {"type": "string"}
    },
    "required": ["url"]
}

# region Rutas


@blue_print.route("/", methods=["GET"])
@blue_print.route("/home", methods=["GET"])
def init():
    """
        Ruta home que recibira al usuario
        :return: Retorna la respuesta con codigo 200 si esta satisfactoriamente conectado
        :treturn: Json
    """
    return jsonify(respuesta="Acortador de RUTAS ML, para obtener el JWT debes iniciar sesion primero"), 200


@blue_print.route("/auth/register", methods=["POST"])
@expects_json(SCHEMA_USUARIOS)
def registrar_usuario():
    """
        Ruta registra usuario
        :return: Retorna la respuesta con codigo 201 si esta satisfactoriamente creado y 400 si no
        :treturn: Json
    """
    try:
        # obtener datos de la tabla
        usuario = request.json.get("usuario")
        clave = request.json.get("clave")
        cantidad_de_ingresos = 0
        if not usuario or not clave:
            current_app.logger.debug('Campos invalidos')
            return jsonify(respuesta="Campos invalidos"), 400
        # existe usuario
        existe_usuario = UsuarioMl.query.filter_by(usuario=usuario).first()
        if existe_usuario:
            current_app.logger.debug('El usuario ya existe')
            return jsonify(respuesta="Usuario ya existe")
        else:
            # Encriptamos clave del usuario
            current_app.logger.debug('Encriptamos clave')
            clave_encriptada = bcrypt.hashpw(
                clave.encode("utf-8"), bcrypt.gensalt())
            fecha_de_creacion = datetime.today()
            current_app.logger.debug(
                f'Insertando fecha de creacion {str(fecha_de_creacion)}')
            # creamos el modelo
            nuevo_usuario = UsuarioMl(
                usuario, clave_encriptada, fecha_de_creacion, cantidad_de_ingresos)
            db.session.add(nuevo_usuario)
            db.session.commit()
            current_app.logger.debug(
                'Usuario nuevo fue creado satisfactoriamente')
            return jsonify(respuesta="Usuario nuevo fue creado satisfactoriamente"), 201
    except Exception as e:
        current_app.logger.debug(f'Error en creacion de usuario {e}')
        abort(500, description=str(e))


@blue_print.route("/auth/login", methods=["POST"])
@expects_json(SCHEMA_USUARIOS)
def iniciar_sesion():
    """
        Ruta login inicia sesion del usuario y devuelve jwt
        :return: Retorna la respuesta con codigo 200 junto con el el jwt, 400 si hubo error
        :treturn: Json
    """
    try:
        # obtener datos de la tabla
        usuario = request.json.get("usuario")
        clave = request.json.get("clave")
        if not usuario or not clave:
            current_app.logger.debug('Campos invalidos')
            return jsonify(respuesta="Campos invalidos"), 400
        # existe usuario
        existe_usuario = UsuarioMl.query.filter_by(usuario=usuario).first()
        if not existe_usuario:
            current_app.logger.debug('Usuario no encontrado')
            return jsonify(respuesta="Usuario no encontrado"), 400
        es_clave_valida = bcrypt.checkpw(clave.encode(
            "utf-8"), existe_usuario.clave.encode("utf-8"))
        if es_clave_valida:
            current_app.logger.debug(f'Clave valida')
            access_token = create_access_token(
                identity=usuario)  # creo access token
            existe_usuario.cantidad_ingresos = UsuarioMl.cantidad_ingresos + 1
            db.session.commit()
            return jsonify(access_token=access_token), 200
        current_app.logger.debug('Clave o usuario incorrecto')
        abort(404, description='Clave o usuario incorrecto')
    except Exception as e:
        current_app.logger.debug(f'Error en inicio de sesion {e}')
        abort(500, description=str(e))


@blue_print.route("/get/users", methods=["GET"])
def obtener_usuarios():
    """
        Ruta obtiene usuarios
        :return: Retorna la respuesta con codigo 200 si obtuvo usuario y 400 si no
        :treturn: Json
    """
    try:
        usuario = UsuarioMl.query.with_entities(UsuarioMl.usuario).all()

        if usuario:
            current_app.logger.debug('Usuario encontrado')
            usuarios_json = usuarios_schema.dump(usuario)
            return jsonify(usuarios_json), 200
        else:
            current_app.logger.debug('No se encontro el usuario')
            abort(404, description='No se encontro el usuario')
    except Exception as e:
        current_app.logger.debug(f'Error al obtener usuarios{e}')
        abort(500, description=str(e))


# RUTAS PROTEGIDAS POR JWT (json web token), RUTAS

@blue_print.route("/add/url", methods=["POST"])
@jwt_required()
@expects_json(SCHEMA_RUTAS)
def crear_ruta():
    """
        Ruta crea ruta corta
        :return: Retorna la respuesta con codigo 201 si esta satisfactoriamente creado y 404 si no
        :treturn: Json
    """
    try:
        url = request.json["url"]
        hashp1 = Utils(str(url))
        validate_url = hashp1.validate_url()
        if validate_url == True:
            uuid = hashp1.uuid_conversor()
            ruta = Rutas.query.filter_by(shortUrl=uuid).first()
            current_app.logger.debug(f'Ruta {str(ruta)}')
            while ruta != None:
                current_app.logger.debug(
                    f'ruta {str(ruta)} encontrada, se vuelve a buscar')
                uuid = hashp1.uuid_conversor()
                ruta = Rutas.query.filter_by(shortUrl=uuid).first()
            fecha_de_creacion = datetime.today()
            nueva_ruta = Rutas(url, uuid, fecha_de_creacion)
            db.session.add(nueva_ruta)
            db.session.commit()
            current_app.logger.debug('Ruta almacenada exitosamente')
            return jsonify(respuesta="Ruta almacenada exitosamente"), 201
        else:
            current_app.logger.debug(f'La ruta {str(url)} no es valida')
            return jsonify(respuesta='La ruta no es valida'), 404
    except Exception as e:
        current_app.logger.debug(f'Error al añadir ruta {e}')
        abort(500, description=str(e))


@blue_print.route("/get/urls", methods=["GET"])
@jwt_required()
def obtener_rutas():
    """
        Obtiene rutas
        :return: Retorna la respuesta con codigo 200 si obtuvo ruta y 400 si no
        :treturn: Json
    """
    try:
        rutas = Rutas.query.all()
        if rutas:
            respuesta = rutas_schema.dump(rutas)
            current_app.logger.debug(f'Se encontro la ruta')
            return jsonify(respuesta), 200
        else:
            current_app.logger.debug('No se encontraron rutas')
            return jsonify(respuesta='No se encontraron rutas'), 404
    except Exception as e:
        current_app.logger.debug(f'Error al obtener rutas{e}')
        abort(500, description=str(e))


@blue_print.route("/get/ruta-por-id/<int:id>", methods=["GET"])
@jwt_required()
def obtener_ruta_por_id(id):
    """
       obtiene ruta por id
        :return: Retorna la respuesta con codigo 200 si obtuvo ruta y 404 si no
        :treturn: Json
    """
    try:
        ruta = Rutas.query.filter_by(id=id).first()
        current_app.logger.debug(f'{ruta}')
        if ruta:
            respuesta = ruta_schema.dump(ruta)
            current_app.logger.debug(f'Se encontro la ruta con el id {id}')
            return jsonify(respuesta), 200
        else:
            current_app.logger.debug(f'No se encontraron rutas con el id {id}')
            return jsonify(respuesta=f'No se encontraron rutas con el {id}'), 404
    except Exception as e:
        current_app.logger.debug(f'Error al obtener rutas {e}')
        abort(500, description=str(e))


@blue_print.route("/get/ruta-larga/<string:short>", methods=["GET"])
@jwt_required()
def obtener_ruta_larga(short):
    """
        Obtiene ruta larga
        :return: Retorna la respuesta con codigo 200 si obtuvo ruta larga y 404 si no
        :treturn: Json
    """
    try:
        ruta = Rutas.query.filter_by(shortUrl=short).first()
        if ruta:
            respuesta = ruta_schema.dump(ruta)
            current_app.logger.debug(f'Se encontro la ruta {str(respuesta)}')
            return jsonify(respuesta=respuesta["url"]), 200
        else:
            current_app.logger.debug(f'No se encontro la ruta')
            return jsonify(respuesta='No se encontro la ruta'), 404
    except Exception as e:
        current_app.logger.debug(f'Error al obtener ruta {e}')
        abort(500, description=str(e))


@blue_print.route("/get/url-short", methods=["GET"])
@jwt_required()
@expects_json(SCHEMA_RUTAS)
def obtener_ruta_corta():
    """
        Obtiene ruta corta
        :return: Retorna la respuesta con codigo 200 si obtuvo ruta corta y 404 si no
        :treturn: Json
    """
    try:
        url = request.json["url"]
        current_app.logger.debug(f'Url {url}')
        ruta = Rutas.query.filter_by(url=url).first()
        current_app.logger.debug(f'Se obtuvo: {ruta}')
        if ruta:
            respuesta = ruta_schema.dump(ruta)
            current_app.logger.debug(f'Se encontro la ruta {str(respuesta)}')
            return jsonify(respuesta=respuesta["shortUrl"]), 200
        else:
            current_app.logger.debug(f'No se encontro la ruta')
            return jsonify(respuesta='No se encontro la ruta'), 404
    except Exception as e:
        current_app.logger.debug(f'Error al obtener ruta {e}')
        abort(500, description=str(e))


@blue_print.route("/delete/url-short/<string:short>", methods=["DELETE"])
@jwt_required()
def eliminar_ruta(short):
    """
        Elimina ruta
        :return: Retorna la respuesta con codigo 200 si se elimino y 404 si no
        :treturn: Json
    """
    try:
        rutas = Rutas.query.filter_by(shortUrl=short).first()
        if rutas:
            db.session.delete(rutas)
            db.session.commit()
            current_app.logger.debug('Ruta eliminada correctamente')
            return jsonify(respuesta="Ruta eliminada correctamente"), 200
        else:
            current_app.logger.debug('No se encontro la ruta')
            return jsonify(respuesta='No se encontro la ruta'), 404
    except Exception as e:
        current_app.logger.debug(f'Error al eliminar ruta{e}')
        abort(500, description=str(e))
#endregion


@blue_print.route("/<string:short>", methods=["GET"])
def redireccionar_ruta_larga(short):
    """
        Redirecciona ruta
        :return: Retorna la respuesta con codigo 400 o redirecciona a la ruta larga
        :treturn: Json
    """
    try:
        ruta = Rutas.query.filter_by(shortUrl=short).first()
        if ruta:
            respuesta = ruta_schema.dump(ruta)
            current_app.logger.debug(f'Se encontro la ruta {str(respuesta)}')
            return redirect(respuesta["url"], code=302)
        else:
            current_app.logger.debug(f'No se encontro la ruta')
            return jsonify(respuesta='No se encontro la ruta'), 404
    except Exception as e:
        current_app.logger.debug(f'Error al obtener ruta {e}')
        abort(500, description=str(e))

# region errorHandler


@blue_print.errorhandler(404)
def process_not_found(e):
    """
        Error handler 404.
        :returns: Returna un json con el error 404
        :treturn: json
    """
    return jsonify(error=str(e)), 404


@blue_print.errorhandler(500)
def error_not_expected(e):
    """
    Error handler 500.
    :returns: Returna un json con el error 500
    :treturn: json
    """
    return jsonify(error=str(e)), 500
#endregion
