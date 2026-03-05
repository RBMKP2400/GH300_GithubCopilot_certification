---
applyTo: "frontend/**"
---
# Octofit-tracker Fitness App React frontend Guidelines

## REACT Frontend App structure

Make sure in all commands we point to the `frontend` directory

```bash
# Use --yes to avoid the interactive confirmation prompt from npx
npx --yes create-react-app frontend --template cra-template --use-npm

npm install bootstrap --prefix frontend

# Add the Bootstrap CSS import at the very top of src/index.js:
sed -i "1iimport 'bootstrap/dist/css/bootstrap.min.css';" frontend/src/index.js

npm install react-router-dom --prefix frontend

```

## React Router — use HashRouter (not BrowserRouter)

GitHub Codespaces serves the React app behind a reverse proxy. Using `BrowserRouter`
causes navigation to fail because the proxy cannot handle client-side routes like `/users`.
Always use `HashRouter` so routing is handled entirely in the browser via the URL hash (`#/users`).

```jsx
import { HashRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
```

## Add proxy to package.json

After creating the React app, add a `proxy` entry to `frontend/package.json` so the React
dev server forwards `/api/*` requests to Django on port 8000. This avoids CORS issues and
works regardless of port visibility settings in the Codespace.

```json
{
  "proxy": "http://localhost:8000"
}
```

## API URL pattern for components

Each component must include the full Codespace URL for the GitHub Actions workflow checks,
but the fallback (when `REACT_APP_CODESPACE_NAME` is not set) must use a **relative path**
so the React proxy handles it:

```js
const CODESPACE_NAME = process.env.REACT_APP_CODESPACE_NAME;
const API_URL = CODESPACE_NAME
  ? `https://${CODESPACE_NAME}-8000.app.github.dev/api/<endpoint>`
  : '/api/<endpoint>';
```

Never use `http://localhost:8000/api/...` as fallback — it fails when the app is accessed
from the public Codespace URL.

## Port visibility

After starting services, ensure port 8000 is public. Add this after starting the Django server:

```bash
gh cs ports visibility 8000:public -c "$CODESPACE_NAME"
```

## Images for the OctoFit Tracker App

The image to use for the app is in the root of this repository docs/octofitapp-small.png

