# Challenge mercado libre


> **_IMPORTANTE!!!:_**  EN EL ARCHIVO Consultas Insomnia.json SE ENCUENTRAN TODAS LAS CONSULTAS EN FORMATO JSON PARA IMPORTAR DIRECTAMENTE EN INSOMNIA Y HACER TODAS LAS CONSULTAS DESDE LA HERRAMIENTA DE PETICIONES

---

# Lenguaje, framework y orm utilizados :notebook_with_decorative_cover:

<ol>
  <li>Python</li>
  <li>flask</li>
  <li>Flask_SQLALCHEMY</li>
</ol>

# ¿Como levantar la api? :rocket:

Se debe crear un virtual env con las librerias colocadas en el archivo requirements.txt.
Dentro de la consola se debe ejecutar los siguientes comandos

`python -m venv venv`
`pip install -r requirements.txt`


# ¿Como probar la api? :test_tube:

Se dejo un archivo .json con las consultas ya hechas en Insomnia. Solo debe importarse ese archivo en insomnia y las consultas pueden generarse desde ahi.

Se dejo un archivo <u>test_unitario.py</u> donde se encuentran algunos test unitarios para ejecutar la api

Tambien se pueden probar utilizando curl, estos son algunos ejemplos:

### Get home
`curl http://localhost:5000/api/ML/home`

### Insert user

`curl http://localhost:5000/api/ML/auth/register --request POST --header "Content-Type: application/json" --data "{\"usuario\":\"Rodri\",\"clave\":\"Salon3232\"}"`


### Login user

`curl http://localhost:5000/api/ML/auth/login --request POST --header "Content-Type: application/json" --data "{\"usuario\":\"Rodri\",\"clave\":\"Salon3232\"}"`

### Get users
`curl http://localhost:5000/api/ML/get/users`



# ¿Como testear la aplicacion? :alembic:


Dentro del archivo test_unitario.py, se encuentran tests unitarios.

Para ejecutar el testeo unitario se debe ejecutar en el cmd el siguiente comando

`python -m unittest`

O se puede correr directamente el script desde cualquier id


# ¿Como ejecutar el dockerfile? :whale:

Se dejo un Dockerfile y un dockerfile para poder ejecutar la api en cualquier SO.
Se deben ejecutar los siguientes comandos:

`docker build -t nombre_imagen .` (construye una imagen a partir de un Docker file)
docker run -it nombreimagen . (corre imagen de forma interactiva todo en minuscula, tengo que colocar el punto despues del nombreimagen)