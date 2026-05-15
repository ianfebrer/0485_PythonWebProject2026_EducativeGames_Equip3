# 0485_PythonWebProject2026_EducativeGames_Equip3

Aplicacion web Flask de juegos educativos con autenticacion, perfil de usuario y ranking por juego.

## Estado actual de persistencia

- Usuarios y perfil: `data/results.json`
- Ranking y mejores puntuaciones: MongoDB externo
- Migracion inicial: si `data/scores.json` existe y la coleccion esta vacia, se importan sus datos automaticamente la primera vez que arranca la app con MongoDB configurado

## Configuracion de base de datos

La capa de ranking usa estas variables de entorno:

- `MONGODB_URI`
- `MONGODB_DB_NAME` (opcional, por defecto `educative_games`)
- `MONGODB_COLLECTION` (opcional, por defecto `game_scores`)

`docker-compose.yml` ya expone esas variables al contenedor `web`.

## Dependencias

Instalacion local:

```bash
pip install -r requirements.txt
```

## Notas de integracion

- La coleccion `game_scores` se usa automaticamente si no indicas otra.
- El backend mantiene la misma API interna (`get_scores_map` y `update_user_score`), asi que no ha sido necesario tocar frontend ni rutas de ranking.
- Si no configuras `MONGODB_URI`, el ranking cae a almacenamiento local en `data/scores.json`.
