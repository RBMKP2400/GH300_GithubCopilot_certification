# 🏋️ OctoFit Tracker

<img src="docs/octofitapp-small.png" alt="OctoFit Tracker" width="200"/>

Aplicación de seguimiento fitness multi-capa construida con **GitHub Copilot Agent Mode**.  
Incluye autenticación de usuarios, registro de actividades, gestión de equipos, clasificación competitiva y sugerencias de entrenamientos.

---

## 🏗️ Arquitectura

```
octofit-tracker/
├── backend/               ← Django REST API + MongoDB
│   ├── manage.py
│   ├── requirements.txt
│   ├── venv/
│   └── src/
│       ├── settings.py    ← Configuración (MongoDB, CORS, ALLOWED_HOSTS)
│       ├── models.py      ← OctoFitUser, Team, Activity, Leaderboard, Workout
│       ├── serializers.py
│       ├── views.py       ← ViewSets + api_root
│       ├── urls.py        ← Router DRF
│       └── management/commands/populate_db.py
└── frontend/              ← React + Bootstrap
    └── src/
        ├── App.js         ← HashRouter + Navbar
        └── components/
            ├── Activities.js
            ├── Leaderboard.js
            ├── Teams.js
            ├── Users.js
            └── Workouts.js
```

| Capa        | Tecnología                          | Puerto |
|-------------|-------------------------------------|--------|
| Backend API | Django 4.1 + Django REST Framework  | 8000   |
| Base datos  | MongoDB (djongo)                    | 27017  |
| Frontend    | React 19 + Bootstrap 5              | 3000   |

---

## 🤖 Creación automática con GitHub Copilot

La forma más rápida de construir esta app es usando **Copilot Agent Mode** en VS Code.  
Abre un Codespace de este repositorio y ejecuta los siguientes prompts en el orden indicado.

### Requisitos previos
- GitHub Codespace abierto (MongoDB ya está corriendo)
- Python venv creado: `python3 -m venv backend/venv`
- Paquetes instalados: `pip install -r backend/requirements.txt`

### Prompt 1 — Crear el proyecto Django
```prompt
/create-django-project
```
> Usa el prompt file `.github/prompts/create-django-project.prompt.md`

### Prompt 2 — Configurar base de datos y poblarla
```prompt
/init-populate-octofit_db
```
> Usa el prompt file `.github/prompts/init-populate-octofit_db.prompt.md`

### Prompt 3 — Actualizar archivos del proyecto Django
```prompt
Let's add the following to a prompt file called `update-octofit-tracker-app.prompt.md`
in the `.github/prompts` directory and add mode: 'agent' and model: GPT-4.1.

# Django App Updates
- All Django project files are in the `octofit-tracker/backend/src` directory.
1. Update settings.py for MongoDB connection and CORS.
2. Update models.py, serializers.py, urls.py, views.py, tests.py, and admin.py
   to support users, teams, activities, leaderboard, and workouts collections.
3. Ensure `/` points to the api and `api_root` is present in `urls.py`.
```

### Prompt 4 — Configurar REST Framework y URLs del codespace
```prompt
Let's setup codespace for the URL, start the server via VS Code launch.json, and test the API.
- All Django project files are in the `octofit-tracker/backend/src` directory.
- Only update urls in settings.py and urls.py
- REST api endpoint format https://$CODESPACE_NAME-8000.app.github.dev/api/[component]/
- Do not hard code the $CODESPACE_NAME value, use the variable
- Update urls.py to replace the return for the REST API URL endpoints with $CODESPACE_NAME
- Update ALLOWED_HOSTS in settings.py with the codespace URL
- Test the API endpoints using curl
```

### Prompt 5 — Instalar React y crear componentes frontend
```prompt
Let's setup the octofit-tracker frontend React framework and ensure everything
is created in the `octofit-tracker/frontend` directory.

1. Create the react app using `npx --yes create-react-app` (--yes avoids interactive prompt).
2. Install react, bootstrap, and react-router-dom
3. Import bootstrap css in src/index.js
4. Add "proxy": "http://localhost:8000" to frontend/package.json
5. Don't change .gitignore
```

### Prompt 6 — Actualizar componentes React
```prompt
Let's update the octofit-tracker frontend React components.
- Use HashRouter (not BrowserRouter) — required for GitHub Codespaces
- For each component use this API URL pattern:
  const CODESPACE_NAME = process.env.REACT_APP_CODESPACE_NAME;
  const API_URL = CODESPACE_NAME
    ? `https://${CODESPACE_NAME}-8000.app.github.dev/api/[component]`
    : '/api/[component]';
  The fallback MUST be a relative path (not http://localhost:8000) so the proxy works.
- Update src/App.js with navigation for all components using react-router-dom.
- Use Bootstrap tables, cards, and navbar.
```

---

## 🛠️ Setup manual paso a paso

### 1. Verificar que MongoDB está corriendo
```bash
ps aux | grep mongod | grep -v grep
```
Si no está corriendo: `sudo mongod --dbpath /data/db --fork --logpath /tmp/mongod.log`

### 2. Configurar el entorno Python
```bash
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

### 3. Crear el proyecto Django
```bash
cd backend && django-admin startproject src . && cd ..
```

### 4. Ejecutar migraciones y poblar la base de datos
```bash
cd backend && source venv/bin/activate
python manage.py makemigrations src
python manage.py migrate
python manage.py populate_db
```

### 5. Iniciar el servidor Django
```bash
cd backend && source venv/bin/activate
nohup python manage.py runserver 0.0.0.0:8000 > /tmp/django.log 2>&1 &
```

### 6. Crear e iniciar la app React
```bash
# Crear la app (--yes evita la confirmación interactiva de npx)
npx --yes create-react-app frontend --template cra-template --use-npm
npm install bootstrap --prefix frontend
npm install react-router-dom --prefix frontend
sed -i "1iimport 'bootstrap/dist/css/bootstrap.min.css';" frontend/src/index.js

# Iniciar el servidor React
cd frontend
REACT_APP_CODESPACE_NAME=$CODESPACE_NAME nohup npm start > /tmp/react.log 2>&1 &
```

### 7. Exponer puertos (Codespaces)
```bash
gh cs ports visibility 8000:public -c "$CODESPACE_NAME"
gh cs ports visibility 3000:public -c "$CODESPACE_NAME"
```

---

## 🌐 Acceso a la aplicación

| Servicio       | URL local              | URL Codespace (ejemplo)                                              |
|----------------|------------------------|----------------------------------------------------------------------|
| React frontend | http://localhost:3000  | `https://<CODESPACE_NAME>-3000.app.github.dev`                       |
| Django API     | http://localhost:8000  | `https://<CODESPACE_NAME>-8000.app.github.dev/api/`                  |

### Endpoints API disponibles
| Endpoint         | Descripción            |
|------------------|------------------------|
| `/api/`          | API root con todos los endpoints |
| `/api/users/`    | Usuarios registrados   |
| `/api/teams/`    | Equipos                |
| `/api/activities/` | Actividades          |
| `/api/leaderboard/` | Clasificación       |
| `/api/workouts/` | Entrenamientos         |

---

## 📋 Ver logs

```bash
# Django (peticiones HTTP, errores)
tail -f /tmp/django.log

# React (compilación, webpack)
tail -f /tmp/react.log

# MongoDB
tail -f /tmp/mongod.log

# Ambos servicios a la vez
tail -f /tmp/django.log /tmp/react.log
```

---

## 🔧 Solución de problemas conocidos

### ❌ `Failed to fetch` en el navegador
El puerto 8000 no es público en el Codespace. Ejecuta:
```bash
gh cs ports visibility 8000:public -c "$CODESPACE_NAME"
```

### ❌ Los botones de navegación no funcionan
El `BrowserRouter` de React no funciona detrás del proxy de Codespaces.  
Asegúrate de que `App.js` usa `HashRouter` de `react-router-dom`.

### ❌ `npx create-react-app` se queda colgado esperando input
Usa el flag `--yes` para saltar la confirmación interactiva:
```bash
npx --yes create-react-app frontend --template cra-template --use-npm
```

### ❌ CORS errors en la consola del navegador
Verifica que `frontend/package.json` tiene el proxy configurado:
```json
"proxy": "http://localhost:8000"
```
Y que los componentes React usan URLs relativas como fallback: `/api/users/` (no `http://localhost:8000/api/users/`).

### ❌ Django no arranca / error de base de datos
Verifica que MongoDB está corriendo:
```bash
ps aux | grep mongod | grep -v grep
```

---

## 📚 Recursos

- [GitHub Copilot Agent Mode](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React Router](https://reactrouter.com/)
- [Djongo (Django + MongoDB)](https://www.djongomapper.com/)

---

&copy; 2025 GitHub &bull; [MIT License](https://gh.io/mit)
