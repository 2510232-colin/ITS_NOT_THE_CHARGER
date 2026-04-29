# TechCare - Guía para clonar BD y correr el proyecto en otra computadora

Este README está pensado para que cualquier compañero haga el proceso completo sin adivinar pasos.

## Objetivo

Con esta guía pueden:

1. Clonar el proyecto desde GitHub.
2. Levantar su entorno local.
3. Crear la base de datos y tablas.
4. Cargar catálogo de servicios base.
5. (Opcional) Importar un respaldo SQL para tener exactamente los mismos datos del equipo.

---

## 1) Requisitos previos

- Python 3.10+
- MySQL Server 8+
- Git

Verificaciones rápidas:

```bash
python3 --version
mysql --version
git --version
```

---

## 2) Clonar repositorio

```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
```

---

## 3) Crear entorno virtual e instalar dependencias

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 4) Configurar `.env`

Copiar archivo de ejemplo:

```bash
cp .env.example .env
```

Editar `.env` con credenciales locales de MySQL:

```dotenv
CLAVE_SECRETA=pon_una_clave_larga_y_segura
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=tu_usuario_mysql
MYSQL_PASSWORD=tu_password_mysql
MYSQL_DATABASE=techcare_db
```

---

## 5) Crear base de datos vacía

Entrar a MySQL y ejecutar:

```sql
CREATE DATABASE IF NOT EXISTS techcare_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Si usan otro nombre, cambien también `MYSQL_DATABASE` en `.env`.

---

## 6) Preparar base de datos del proyecto (recomendado)

Comando principal:

```bash
python scripts/preparar_proyecto.py --demo
```

Este comando aplica:

- esquema base
- migraciones
- catálogo de servicios de ejemplo

Si no quieren datos demo, usen:

```bash
python scripts/preparar_proyecto.py
```

---

## 7) Ejecutar aplicación

```bash
python server.py
```

Abrir en navegador:

- http://127.0.0.1:5000

---

## 8) ¿Cómo tener exactamente la misma BD que el líder del equipo?

Sí se puede. Para eso necesitan un respaldo SQL (`mysqldump`) de la BD del líder.

### A. Exportar respaldo (solo líder)

```bash
mysqldump -u TU_USUARIO -p techcare_db > sql/respaldo_equipo.sql
```

### B. Importar respaldo (cada compañero)

```bash
mysql -u TU_USUARIO -p techcare_db < sql/respaldo_equipo.sql
```

Con eso todos tendrán la misma información (servicios, cambios, etc.) al momento del respaldo.

---

## 9) Flujo recomendado para el equipo

1. El líder comparte cambios por GitHub.
2. Cada compañero hace `git pull`.
3. Si hubo cambios de BD, correr:

```bash
python scripts/preparar_proyecto.py
```

4. Si necesitan estado idéntico, importar `sql/respaldo_equipo.sql` actualizado.

---

## 10) Solución de problemas comunes

### Error de conexión a MySQL

Revisar `.env` y confirmar que MySQL está encendido.

### Error de tabla inexistente

Ejecutar de nuevo:

```bash
python scripts/preparar_proyecto.py
```

### Dependencias faltantes

Activar entorno virtual e instalar:

```bash
pip install -r requirements.txt
```

---

## 11) Buenas prácticas para subir a GitHub

- No subir `.env`.
- Sí subir `.env.example`.
- Si suben `sql/respaldo_equipo.sql`, validar que no tenga datos sensibles reales.
