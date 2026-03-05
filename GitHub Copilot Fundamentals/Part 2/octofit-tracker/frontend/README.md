# OctoFit Tracker — Frontend React

Interfaz de usuario del OctoFit Tracker, construida con React 19 y Bootstrap 5.

---

## Estructura del proyecto

```
frontend/
├── public/
│   └── index.html
└── src/
    ├── index.js           ← Bootstrap CSS import
    ├── App.js             ← HashRouter + Navbar + rutas
    ├── logo.png           ← Logo de la app
    └── components/
        ├── Users.js       ← Listado de usuarios
        ├── Teams.js       ← Equipos
        ├── Activities.js  ← Actividades registradas
        ├── Leaderboard.js ← Clasificación
        └── Workouts.js    ← Entrenamientos sugeridos
```

---

## Requisitos

- Node.js 18+
- npm 9+
- El servidor Django corriendo en el puerto 8000

---

## Instalación

```bash
# Desde la raíz del repositorio (octofit-tracker/)
npx --yes create-react-app frontend --template cra-template --use-npm
npm install bootstrap --prefix frontend
npm install react-router-dom --prefix frontend

# Añadir Bootstrap CSS al inicio de src/index.js
sed -i "1iimport 'bootstrap/dist/css/bootstrap.min.css';" frontend/src/index.js
```

---

## Iniciar el servidor de desarrollo

### En entorno local
```bash
cd frontend
npm start
```

### En GitHub Codespaces (modo persistente)
```bash
cd frontend
REACT_APP_CODESPACE_NAME=$CODESPACE_NAME \
  nohup npm start > /tmp/react.log 2>&1 &

# Verificar que está corriendo
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
```

### Exponer el puerto 3000
```bash
gh cs ports visibility 3000:public -c "$CODESPACE_NAME"
```

---

## Variables de entorno

| Variable                    | Descripción                                  | Ejemplo                                  |
|-----------------------------|----------------------------------------------|------------------------------------------|
| `REACT_APP_CODESPACE_NAME`  | Nombre del Codespace de GitHub (opcional)    | `opulent-space-potato-x7vr4rgjvw42pq`   |

Si la variable no está definida, los componentes usan URLs relativas (`/api/...`) y el proxy de `package.json` enruta al backend local.

---

## Proxy hacia el backend

`package.json` incluye esta configuración para enrutar peticiones API:

```json
"proxy": "http://localhost:8000"
```

Con esto, llamar a `/api/users/` en el frontend se traduce automáticamente a `http://localhost:8000/api/users/` sin necesidad de CORS.

---

## Rutas disponibles

| Ruta              | Componente      | Descripción             |
|-------------------|-----------------|-------------------------|
| `/#/`             | Home            | Pantalla de inicio      |
| `/#/users`        | Users           | Lista de usuarios       |
| `/#/teams`        | Teams           | Gestión de equipos      |
| `/#/activities`   | Activities      | Actividades registradas |
| `/#/leaderboard`  | Leaderboard     | Clasificación           |
| `/#/workouts`     | Workouts        | Entrenamientos          |

> ℹ️ Se usa `HashRouter` (rutas con `#`) para compatibilidad con el proxy inverso de GitHub Codespaces. `BrowserRouter` causa errores 404 al navegar.

---

## Ver logs

```bash
tail -f /tmp/react.log
```

---

## Build de producción

```bash
npm run build --prefix frontend
```

Los archivos estáticos se generan en `frontend/build/`.
