# IT'S NOT THE CHARGER

Aplicación web Flask para operación de tickets y atención de servicios técnicos.

## Ejecución rápida

1. Activar entorno virtual.
2. Configurar variables en `.env`:
   - `CLAVE_SECRETA`
   - `MYSQL_HOST`
   - `MYSQL_PORT`
   - `MYSQL_USER`
   - `MYSQL_PASSWORD`
   - `MYSQL_DATABASE`
3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Ejecutar aplicación:

```bash
python server.py
```

La app corre en `http://127.0.0.1:8080`.

## Estructura principal

- `server.py`: arranque de la app
- `routes_public.py`: rutas públicas
- `routes_auth.py`: autenticación
- `panel_routes.py`: paneles y operaciones por rol
- `app_core.py`: lógica compartida
- `db.py`: conexión y consultas MySQL
- `validaciones.py`: validaciones de entrada
- `templates/` y `static/`: interfaz
