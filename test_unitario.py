import unittest
from app import app, db
from models.model import Rutas, UsuarioMl
from datetime import datetime
from schemas.schema import ruta_schema, usuarios_schema, rutas_schema


class ApiTest(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        # Crea un contexto de aplicación
        with self.app.app_context():
            # Crea las tablas de la base de datos
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            db.session.remove()
            db.drop_all()

    def test_get_index(self):
        """
            Get index
        """
        res = self.client.get('/api/ML/home')
        json_data = res.get_json()
        self.assertEqual(200, res.status_code)
        self.assertIn(
            "Acortador de RUTAS ML, para obtener el JWT debes iniciar sesion primero", json_data["respuesta"])

    def test_post_user(self):
        """
            Testea el post del user
        """
        with self.app.app_context():
            res = self.client.post(
                "/api/ML/auth/register", json={'clave': 'clave1', 'usuario': 'user'})
            json_data = res.get_json()
            self.assertEqual(201, res.status_code)
            self.assertIn(
                'Usuario nuevo fue creado satisfactoriamente', json_data["respuesta"])

    def test_obtain_jwt(self):
        """
            Testea obtener jwt
        """
        with self.app.app_context():
            self.client.post("/api/ML/auth/register",
                             json={'clave': 'clave1', 'usuario': 'user'})
            res = self.client.post("/api/ML/auth/login",
                                   json={'clave': 'clave1', 'usuario': 'user'})
            json_data = res.get_json()
            self.assertEqual(200, res.status_code)
            self.assertIn("access_token", dict(json_data).keys())

    def test_post_route(self):
        """
            Testea post a la tabla route
        """
        with self.app.app_context():
            self.client.post("/api/ML/auth/register",
                             json={'clave': 'clave1', 'usuario': 'user'})
            res = self.client.post("/api/ML/auth/login",
                                   json={'clave': 'clave1', 'usuario': 'user'})
            json_data = res.get_json()
            res = self.client.post("/api/ML/add/url", json={'url': 'https://ww.prueba.com'}, headers={
                                   'Authorization': f'Bearer {json_data["access_token"]}'})
            json_data = res.get_json()
            self.assertEqual(201, res.status_code)
            self.assertIn("Ruta almacenada exitosamente",
                          json_data["respuesta"])

    def test_get_routes(self):
        """
            Testea get a la tabla route
        """
        with self.app.app_context():
            self.client.post("/api/ML/auth/register",
                             json={'clave': 'clave1', 'usuario': 'user'})
            res = self.client.post("/api/ML/auth/login",
                                   json={'clave': 'clave1', 'usuario': 'user'})
            json_data = res.get_json()
            self.client.post("/api/ML/add/url", json={'url': 'https://ww.prueba.com'}, headers={
                                   'Authorization': f'Bearer {json_data["access_token"]}'})
            res = self.client.get("/api/ML/get/urls", headers={
                                   'Authorization': f'Bearer {json_data["access_token"]}'})
            self.assertEqual(200, res.status_code)
    
    def test_get_route_by_id(self):
        """
            Testea get a la tabla route por id
        """
        with self.app.app_context():
            self.client.post("/api/ML/auth/register",
                             json={'clave': 'clave1', 'usuario': 'user'})
            res = self.client.post("/api/ML/auth/login",
                                   json={'clave': 'clave1', 'usuario': 'user'})
            json_data = res.get_json()
            self.client.post("/api/ML/add/url", json={'url': 'https://ww.prueba.com'}, headers={
                                   'Authorization': f'Bearer {json_data["access_token"]}'})

            res = self.client.get("/api/ML/get/ruta-por-id/1", headers={
                                   'Authorization': f'Bearer {json_data["access_token"]}'})
            print(res)
            self.assertEqual(200, res.status_code)
            self.assertIn("Se encontro la ruta con el id 1",
                          json_data["respuesta"])