# Checklist final - Render + Aiven (producción académica)

## 1) Estado del deploy
- [ ] El servicio en Render está en estado **Live**.
- [ ] El Start Command es `gunicorn server:app`.
- [ ] La URL pública abre correctamente.

## 2) Variables de entorno en Render
- [ ] `CLAVE_SECRETA` configurada.
- [ ] `MYSQL_HOST` configurada.
- [ ] `MYSQL_PORT` configurada.
- [ ] `MYSQL_USER` configurada.
- [ ] `MYSQL_PASSWORD` configurada.
- [ ] `MYSQL_DATABASE` configurada.
- [ ] `MYSQL_SSL_MODE=VERIFY_CA` (o `REQUIRED` si aplica en tu configuración).
- [ ] `MYSQL_SSL_CA=/opt/render/project/src/cert/aiven-ca.pem`.

## 3) Base de datos (Aiven)
- [ ] La base está en estado **Running**.
- [ ] Se importó el respaldo SQL (`respaldo_local.sql`).
- [ ] Existen tablas clave (`usuarios`, `tickets`, `servicios`, `productos`).
- [ ] El login funciona con usuario existente.

## 4) Pruebas funcionales mínimas
- [ ] Inicio de sesión cliente/admin.
- [ ] Listado de servicios y detalle de servicio.
- [ ] Creación de ticket desde cotización.
- [ ] Panel de tickets carga sin error.
- [ ] Cambio de estado de ticket (técnico/admin).
- [ ] Cierre de sesión.

## 5) Seguridad básica antes de presentar
- [ ] Rotar contraseña de Aiven si fue compartida públicamente.
- [ ] Actualizar `MYSQL_PASSWORD` en Render después de rotar.
- [ ] Confirmar que `.env` no está en Git.
- [ ] Confirmar que `respaldo_local.sql` no está en Git.

## 6) Estabilidad para demo
- [ ] Probar app en modo incógnito.
- [ ] Probar desde red distinta (datos móviles o equipo externo).
- [ ] Tener un usuario de respaldo para demo.
- [ ] Tener 2–3 tickets de ejemplo listos para mostrar flujo.

## 7) Si algo falla durante demo
- [ ] Revisar pestaña **Logs** en Render.
- [ ] Verificar que no haya cambios recientes sin deploy.
- [ ] Confirmar variables de entorno sin espacios extra.
- [ ] Verificar conectividad de Aiven y estado del servicio.

## Comandos útiles rápidos
```bash
# Ver cambios locales
git status

# Guardar cambios de cierre
git add .
git commit -m "cierre deploy render"
git push
```
