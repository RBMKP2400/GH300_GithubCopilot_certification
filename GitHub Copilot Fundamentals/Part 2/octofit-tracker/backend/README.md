# OctoFit Tracker — Backend Django

API REST del OctoFit Tracker, construida con Django 4.1, Django REST Framework y MongoDB (via djongo).

---

## Estructura del módulo

```
backend/
├── manage.py
├── requirements.txt
├── venv/
└── src/
    ├── __init__.py
    ├── settings.py                    ← Config principal (MongoDB, CORS, ALLOWED_HOSTS)
    ├── urls.py                        ← Router DRF + api_root
    ├── views.py                       ← 5 ViewSets (usuarios, equipos, actividades, etc.)
    ├── models.py                      ← OctoFitUser, Team, Activity, Leaderboard, Workout
    ├── serializers.py                 ← Serializers DRF (ObjectId → string)
    ├── admin.py                       ← Todos los modelos registrados
    ├── wsgi.py / asgi.py
    └── management/
        └── commands/
            └── populate_db.py         ← Datos de prueba (superhéroes)
```

---

## Requisitos

- Python 3.10+
- MongoDB corriendo en `localhost:27017`
- Paquetes en `requirements.txt`

---

## Setup del entorno

```bash
# 1. Crear el entorno virtual (desde la raíz octofit-tracker/)
python3 -m venv backend/venv

# 2. Activar el entorno
source backend/venv/bin/activate

# 3. Instalar dependencias
pip install -r backend/requirements.txt
```

---

## Base de datos MongoDB

### Verificar que MongoDB está corriendo
```bash
ps aux | grep mongod | grep -v grep
```

Si no está corriendo:
```bash
sudo mongod --dbpath /data/db --fork --logpath /tmp/mongod.log
```

### Ejecutar migraciones
```bash
source backend/venv/bin/activate
cd backend
python manage.py makemigrations src
python manage.py migrate
```
> ℹ️ djongo puede imprimir advertencias sobre NULL/NOT NULL — son no fatales y se pueden ignorar.

### Poblar con datos de prueba
```bash
python manage.py populate_db
```

Crea 8 superhéroes (Marvel + DC), 2 equipos, 8 actividades, 8 entradas en clasificación y 4 entrenamientos.

---

## Iniciar el servidor

```bash
source backend/venv/bin/activate
cd backend
python manage.py runserver 0.0.0.0:8000
```

### En Codespaces (modo persistente)
```bash
cd backend && source venv/bin/activate
nohup python manage.py runserver 0.0.0.0:8000 > /tmp/django.log 2>&1 &

# Exponer el puerto como público
gh cs ports visibility 8000:public -c "$CODESPACE_NAME"
```

---

## Endpoints API

| Método | Endpoint             | Descripción              |
|--------|----------------------|--------------------------|
| GET    | `/api/`              | API root — lista de endpoints |
| GET    | `/api/users/`        | Lista de usuarios        |
| POST   | `/api/users/`        | Crear usuario            |
| GET    | `/api/teams/`        | Lista de equipos         |
| GET    | `/api/activities/`   | Lista de actividades     |
| GET    | `/api/leaderboard/`  | Clasificación            |
| GET    | `/api/workouts/`     | Entrenamientos           |

### Probar con curl
```bash
# API root
curl http://localhost:8000/api/

# Usuarios
curl http://localhost:8000/api/users/

# Desde un Codespace
curl https://$CODESPACE_NAME-8000.app.github.dev/api/users/
```

---

## Variables de entorno importantes

| Variable          | Uso                                          |
|-------------------|----------------------------------------------|
| `CODESPACE_NAME`  | Se lee automáticamente desde el entorno del Codespace. Configura el `ALLOWED_HOSTS` y la URL base de la API en `urls.py`. |

`settings.py` añade el host del Codespace automáticamente:
```python
import os
if os.environ.get('CODESPACE_NAME'):
    ALLOWED_HOSTS.append(f"{os.environ.get('CODESPACE_NAME')}-8000.app.github.dev")
```

---

## Ver logs del servidor

```bash
tail -f /tmp/django.log
```

---

## Panel de administración de Django

```bash
# Crear superusuario (sólo si se necesita)
python manage.py createsuperuser

# Acceder
open http://localhost:8000/admin/
```
