# OctoFit Tracker

Proyecto práctico full-stack para entrenar competencias GH-300 con GitHub Copilot Agent Mode.

La aplicación implementa backend REST con Django + MongoDB y frontend React con navegación y vistas de datos fitness.

---

## Arquitectura

```
octofit-tracker/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   └── src/
│       ├── settings.py
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       └── management/commands/populate_db.py
├── frontend/
│   └── src/
│       ├── App.js
│       └── components/
└── .github/
    ├── prompts/
    ├── steps/
    └── instructions/
```

| Capa | Tecnología | Puerto |
|---|---|---:|
| Backend | Django 4 + Django REST Framework | 8000 |
| Datos | MongoDB (djongo) | 27017 |
| Frontend | React + Bootstrap | 3000 |

---

## Opción A (recomendada): construir con Copilot Agent Mode

Usa los prompts y guía incluidos en `.github/` siguiendo este orden:

1. `.github/prompts/create-django-project.prompt.md`
2. `.github/prompts/init-populate-octofit_db.prompt.md`
3. Pasos guiados en `.github/steps/`

Material de apoyo adicional:

- `.github/instructions/octofit_tracker_setup_project.instructions.md`
- `.github/instructions/octofit_tracker_django_backend.instructions.md`
- `.github/instructions/octofit_tracker_react_frontend.instructions.md`

---

## Opción B: setup manual

### 1) Backend

```bash
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt

cd backend
python manage.py makemigrations src
python manage.py migrate
python manage.py populate_db
python manage.py runserver 0.0.0.0:8000
```

### 2) Frontend

```bash
npx --yes create-react-app frontend --template cra-template --use-npm
npm install bootstrap --prefix frontend
npm install react-router-dom --prefix frontend

cd frontend
npm start
```

---

## Endpoints principales

- `/api/`
- `/api/users/`
- `/api/teams/`
- `/api/activities/`
- `/api/leaderboard/`
- `/api/workouts/`

---

## Ejecución en Codespaces

- Exponer puertos:

```bash
gh cs ports visibility 8000:public -c "$CODESPACE_NAME"
gh cs ports visibility 3000:public -c "$CODESPACE_NAME"
```

- Usar `HashRouter` en frontend para evitar problemas de enrutado con proxy inverso.
- Mantener fallback de API relativo (`/api/...`) para que funcione el proxy local.

---

## Logs y diagnóstico

```bash
tail -f /tmp/django.log
tail -f /tmp/react.log
tail -f /tmp/mongod.log
```

Problemas frecuentes:

- `Failed to fetch`: puerto 8000 no público en Codespace.
- Navegación rota: uso de `BrowserRouter` en lugar de `HashRouter`.
- Error CORS: revisar proxy en frontend y URL fallback relativa.

---

## Referencias internas

- Backend: [backend/README.md](backend/README.md)
- Frontend: [frontend/README.md](frontend/README.md)

---

## Recursos

- [GitHub Copilot Agent Mode](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React](https://react.dev/)
- [React Router](https://reactrouter.com/)
