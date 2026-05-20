# Educative Gamer

Aplicacion web Flask de juegos educativos con autenticacion, perfil de usuario, guardado de mejores puntuaciones y ranking por juego.

El proyecto contiene tres minijuegos:

- `Keyboard Hero`: juego de mecanografia/reaccion.
- `Mouse Master`: juego de precision con el raton.
- `Drag & Drop`: juego de asociacion de figuras.

## Cambios principales del proyecto

Esta version reorganiza el proyecto original en una estructura mas mantenible y separa responsabilidades por capas:

- `routes/`: blueprints de Flask para autenticacion, paginas principales y APIs de juegos.
- `services/`: logica de perfil, ranking y guardado de puntuaciones.
- `storage/`: acceso a datos de usuarios y puntuaciones.
- `games/`: logica propia de cada minijuego.
- `templates/` y `static/`: interfaz HTML, CSS y JavaScript.

Tambien se han incorporado mejoras visuales importantes respecto a la base original:

- Redisenyo global de `static/css/styles.css`.
- Plantillas de login, registro, pagina inicial y juegos con estilos mas coherentes.
- Pantallas de juego mas completas para teclado, raton y drag and drop.
- Navegacion comun mediante `templates/base.html`.

## Persistencia de datos

El estado actual de esta rama usa dos sistemas de persistencia:

- Usuarios y perfil: `data/results.json`.
- Ranking y mejores puntuaciones: MongoDB externo si esta configurado; si no, fallback local en `data/scores.json`.

La capa de puntuaciones mantiene una API interna estable mediante `ScoreStorage`, `ScoreService` y `RankingService`, por lo que las rutas de los juegos solo envian el nombre del usuario, el juego y la puntuacion obtenida.

### MongoDB para ranking

La configuracion de MongoDB se lee desde variables de entorno:

- `MONGODB_URI`: cadena de conexion.
- `MONGODB_DB_NAME`: nombre de base de datos. Por defecto, `educative_games`.
- `MONGODB_COLLECTION`: coleccion de puntuaciones. Por defecto, `game_scores`.

Si `MONGODB_URI` no existe o contiene credenciales placeholder, la aplicacion usa `data/scores.json`.

Cuando MongoDB esta configurado y la coleccion esta vacia, `storage/score_storage.py` importa automaticamente los datos existentes de `data/scores.json`.

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

Crear un archivo `.env` si se quiere configurar MongoDB:

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

El contenedor expone el puerto `5000` y monta `./data` dentro de `/app/data` para conservar los JSON locales.

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
├── data/
│   ├── results.json
│   └── scores.json
├── games/
├── models/
├── routes/
├── services/
├── storage/
├── static/
├── templates/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Observaciones tecnicas

- Las contrasenas de usuario se guardan hasheadas mediante Werkzeug.
- El ranking guarda solo la mejor puntuacion por usuario y juego.
- Si un usuario no ha jugado a un juego, su puntuacion aparece como `0`.
- La sesion de Flask se usa para identificar al usuario autenticado durante el guardado de resultados.
