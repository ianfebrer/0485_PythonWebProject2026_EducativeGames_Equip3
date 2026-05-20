# Educative Gamer

Aplicacion web Flask de juegos educativos con autenticacion, perfil de usuario, guardado de mejores puntuaciones y ranking por juego.

El proyecto contiene tres minijuegos:

- `Keyboard Hero`: juego de mecanografia/reaccion.
- `Mouse Master`: juego de precision con el raton.
- `Drag & Drop`: juego de asociacion de figuras.

## Cambios principales del proyecto

<<<<<<< HEAD
Esta version reorganiza el proyecto original en una estructura mas mantenible y separa responsabilidades por capas:

- `routes/`: blueprints de Flask para autenticacion, paginas principales y APIs de juegos.
- `services/`: logica de perfil, ranking y guardado de puntuaciones.
- `storage/`: acceso a datos de usuarios y puntuaciones.
- `games/`: logica propia de cada minijuego.
- `templates/` y `static/`: interfaz HTML, CSS y JavaScript.

Tambien se han incorporado mejoras visuales importantes respecto a la base original:

- Redisenyo global de `static/css/styles.css`.
- Plantillas de login, registro, pagina inicial y juegos con estilos mas coherentes.
=======
Esta version profesionaliza la estructura original y separa responsabilidades por capas:

- `routes/`: blueprints de Flask para autenticacion, paginas principales y APIs de juegos.
- `services/`: logica de perfil, ranking y guardado de puntuaciones.
- `storage/`: acceso a datos persistentes.
- `models/`: modelos de dominio y modelo SQLAlchemy de usuario.
- `games/`: logica propia de cada minijuego.
- `templates/` y `static/`: interfaz HTML, CSS y JavaScript.

Tambien se han incorporado mejoras visuales importantes:

- Redisenyo global de `static/css/styles.css`.
- Plantillas de login, registro, pagina inicial, perfil, ranking y juegos con estilos mas coherentes.
>>>>>>> e90c375 (Actualización del readme)
- Pantallas de juego mas completas para teclado, raton y drag and drop.
- Navegacion comun mediante `templates/base.html`.

## Persistencia de datos

<<<<<<< HEAD
El estado actual de esta rama usa dos sistemas de persistencia:

- Usuarios y perfil: `data/results.json`.
- Ranking y mejores puntuaciones: MongoDB externo si esta configurado; si no, fallback local en `data/scores.json`.

La capa de puntuaciones mantiene una API interna estable mediante `ScoreStorage`, `ScoreService` y `RankingService`, por lo que las rutas de los juegos solo envian el nombre del usuario, el juego y la puntuacion obtenida.

### MongoDB para ranking

La configuracion de MongoDB se lee desde variables de entorno:
=======
El proyecto usa dos bases de datos segun el tipo de informacion:

- Usuarios y perfil: MariaDB remota mediante Flask-SQLAlchemy y PyMySQL.
- Ranking y mejores puntuaciones: MongoDB mediante PyMongo.

Los antiguos ficheros JSON dejan de ser la fuente principal de datos. `data/results.json` solo queda como referencia heredada en algunos parametros por compatibilidad, pero `storage/user_storage.py` trabaja contra MariaDB.

## MariaDB para usuarios

La conexion a MariaDB se configura en `app.py`:

```python
mysql+pymysql://arnau:...@158.179.217.136:3307/appdb
```

La instancia de SQLAlchemy se centraliza en `extensions.py`:

```python
db = SQLAlchemy()
```

`app.py` inicializa la extension con:

```python
db.init_app(app)
```

El modelo principal es `models/user.py`. La clase `User` hereda de `db.Model` y usa la tabla `usuaris`.

Campos principales:

- `id`: clave primaria autoincremental.
- `username`: nombre de usuario unico y obligatorio.
- `password_hash`: contrasena hasheada con Werkzeug.
- `total_score`: puntuacion total heredada del modelo anterior.
- `anotacions`: notas del perfil del usuario.
- `vist`: indicador booleano usado en el perfil.
- `created_at`: fecha de creacion del usuario.

La capa `storage/user_storage.py` encapsula las operaciones de usuario:

- `load_users()`: obtiene todos los usuarios con `User.query.all()`.
- `get_user(username)`: busca un usuario con `User.query.filter_by(...).first()`.
- `add_user(new_user)`: inserta un usuario con `db.session.add()` y `db.session.commit()`.
- `update_user(updated_user)`: confirma cambios pendientes en la sesion.

## MongoDB para ranking

Las puntuaciones de los juegos se guardan en MongoDB. La configuracion se lee desde variables de entorno:
>>>>>>> e90c375 (Actualización del readme)

- `MONGODB_URI`: cadena de conexion.
- `MONGODB_DB_NAME`: nombre de base de datos. Por defecto, `educative_games`.
- `MONGODB_COLLECTION`: coleccion de puntuaciones. Por defecto, `game_scores`.

<<<<<<< HEAD
Si `MONGODB_URI` no existe o contiene credenciales placeholder, la aplicacion usa `data/scores.json`.

Cuando MongoDB esta configurado y la coleccion esta vacia, `storage/score_storage.py` importa automaticamente los datos existentes de `data/scores.json`.
=======
`storage/score_storage.py` crea un indice unico por `username` y guarda las mejores puntuaciones por usuario en un mapa con estas claves:

- `teclado`
- `raton`
- `drag_drop`

El ranking muestra la mejor puntuacion de cada usuario por juego y ordena por puntuacion descendente.
>>>>>>> e90c375 (Actualización del readme)

## Instalacion local

Crear y activar entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

<<<<<<< HEAD
Crear un archivo `.env` si se quiere configurar MongoDB:
=======
Crear un archivo `.env` para MongoDB:
>>>>>>> e90c375 (Actualización del readme)

```env
MONGODB_URI=mongodb+srv://usuario:password@cluster/...
MONGODB_DB_NAME=educative_games
MONGODB_COLLECTION=game_scores
```

Ejecutar la aplicacion:

```bash
python app.py
```

La aplicacion queda disponible en:

```text
http://localhost:5000
```

## Ejecucion con Docker

El proyecto incluye `Dockerfile` y `docker-compose.yml`.

```bash
docker compose up --build
```

<<<<<<< HEAD
El contenedor expone el puerto `5000` y monta `./data` dentro de `/app/data` para conservar los JSON locales.
=======
El contenedor expone el puerto `5000` y recibe la configuracion de MongoDB desde variables de entorno.
>>>>>>> e90c375 (Actualización del readme)

## Rutas principales

- `/`: pagina inicial.
- `/register`: registro de usuario.
- `/login`: inicio de sesion.
- `/logout`: cierre de sesion.
- `/perfil`: perfil del usuario autenticado.
- `/ranking`: ranking por juego.
- `/mecanografia`: Keyboard Hero.
- `/joc-rato`: Mouse Master.
- `/game/drag-and-drop`: Drag & Drop.

## APIs internas

- `/api/get-frase`: obtiene una frase para el juego de teclado.
- `/api/guardar-resultat`: guarda puntuacion de teclado.
- `/api/mouse-objectiu`: obtiene objetivo del juego de raton.
- `/api/mouse-validar`: valida una respuesta del juego de raton.
- `/api/guardar-resultat-rato`: guarda puntuacion de raton.
- `/api/validate_move`: valida una accion de drag and drop.
- `/api/save_score`: guarda puntuacion de drag and drop.

## Estructura resumida

```text
.
├── app.py
├── config.py
<<<<<<< HEAD
├── data/
│   ├── results.json
│   └── scores.json
├── games/
├── models/
├── routes/
├── services/
├── storage/
=======
├── extensions.py
├── games/
├── models/
│   └── user.py
├── routes/
├── services/
├── storage/
│   ├── user_storage.py
│   └── score_storage.py
>>>>>>> e90c375 (Actualización del readme)
├── static/
├── templates/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Observaciones tecnicas

<<<<<<< HEAD
- Las contrasenas de usuario se guardan hasheadas mediante Werkzeug.
- El ranking guarda solo la mejor puntuacion por usuario y juego.
- Si un usuario no ha jugado a un juego, su puntuacion aparece como `0`.
- La sesion de Flask se usa para identificar al usuario autenticado durante el guardado de resultados.
=======
- Las contrasenas de usuario no se guardan en texto plano; se almacenan hasheadas.
- MariaDB gestiona usuarios, login y datos de perfil.
- MongoDB gestiona las mejores puntuaciones y el ranking.
- La sesion de Flask identifica al usuario autenticado durante el guardado de resultados.
- `storage/user_storage.py` mantiene un parametro `file_path` por compatibilidad con codigo anterior, pero ya no usa JSON para guardar usuarios.
>>>>>>> e90c375 (Actualización del readme)
