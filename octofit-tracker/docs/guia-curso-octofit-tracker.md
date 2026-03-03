# 📚 Guía de Aprendizaje: Build Applications with GitHub Copilot Agent Mode

> Basada en el repositorio de ejercicios para la certificación GH-300 de GitHub Copilot.

---

## 🎯 Objetivo del Curso

Aprender a usar **GitHub Copilot en modo Agent** para construir desde cero una aplicación web multi-tier (**OctoFit Tracker**) utilizando React + Django + MongoDB, todo dentro de **GitHub Codespaces**.

La aplicación que construirás incluirá:

- Perfiles y autenticación de usuarios
- Registro y seguimiento de actividades físicas
- Creación y gestión de equipos
- Tabla de clasificación competitiva
- Sugerencias de entrenamientos personalizados

---

## 🚀 PRIMEROS PASOS: Configuración con Copilot CLI

> Antes de empezar con el curso en VS Code / Codespaces, puedes usar **GitHub Copilot CLI** desde tu terminal local para explorar el repositorio y prepararte.

### 1. Instalación de Copilot CLI

```bash
# macOS / Linux
curl -fsSL https://gh.io/copilot-install | bash

# Windows (PowerShell con WinGet)
winget install GitHub.Copilot

# Con npm (multiplataforma)
npm install -g @github/copilot
```

> **Requisito:** Necesitas una suscripción activa a GitHub Copilot.

---

### 2. Lanzar Copilot CLI en el repositorio

Navega a la raíz del repositorio clonado y lanza Copilot CLI:

```bash
cd GH300_GithubCopilot_certification/project
copilot
```

En el primer arranque se te pedirá autenticarte con `/login`. Sigue las instrucciones en pantalla.

---

### 3. Comandos iniciales recomendados para el estudiante

Una vez dentro del CLI interactivo, prueba estos comandos para familiarizarte con el proyecto:

#### 🔍 Explorar y entender el proyecto
```
¿Qué hace este proyecto? Explícame la estructura de carpetas
```
```
Lee el fichero docs/octofit_story.md y resume el contexto del proyecto
```
```
¿Qué instrucciones tiene Copilot configuradas en este repositorio?
```
> Copilot CLI lee automáticamente los ficheros `.github/instructions/**/*.instructions.md`  
> Puedes listar las instrucciones activas con el comando:
> ```
> /instructions
> ```

---

#### 🗂️ Revisar los pasos del curso antes de empezar
```
Lee los ficheros en .github/steps/ y dime en qué orden debo completar el curso
```
```
¿Qué tengo que hacer en el Step 2 del curso?
```

---

#### ⚙️ Planificar el trabajo con Copilot
```
/plan Quiero construir el backend Django de OctoFit Tracker con MongoDB. 
¿Qué pasos debo seguir?
```

```
/research ¿Cuáles son las mejores prácticas para conectar Django con MongoDB usando Djongo?
```

---

#### 🛠️ Ejecutar comandos del entorno con ayuda de Copilot
```
Crea el entorno virtual Python en octofit-tracker/backend/venv
```
```
Crea el fichero requirements.txt con las dependencias necesarias para el proyecto
```
```
Instala las dependencias del fichero requirements.txt en el entorno virtual
```

> ⚠️ Copilot CLI te mostrará los comandos **antes de ejecutarlos**.  
> Siempre revisa y aprueba cada acción propuesta.

---

#### 🔄 Cambiar el modelo de IA según la tarea
```
/model
```
> Puedes elegir entre Claude Sonnet 4.x, GPT-5, etc. Para tareas de generación de código  
> extenso, los modelos **GPT-4.1** o **Claude Sonnet** son los recomendados en este curso.

---

#### 📋 Atajos de teclado útiles en el CLI

| Atajo | Acción |
|---|---|
| `Shift+Tab` | Cambiar modo (interactivo → plan) |
| `Ctrl+S` | Ejecutar comando preservando el input |
| `Ctrl+O` | Expandir historial reciente |
| `Ctrl+L` | Limpiar pantalla |
| `!comando` | Ejecutar comando de shell directamente |
| `Esc` | Cancelar operación actual |
| `↑ / ↓` | Navegar historial de comandos |

---

## 📁 MÓDULO 1: `.devcontainer/` — El Entorno de Desarrollo

Esta carpeta configura automáticamente un **contenedor de desarrollo listo para usar** en GitHub Codespaces.

### 📄 `devcontainer.json` — La "receta" del entorno

```
Imagen base: Ubuntu 22.04 (jammy)
```

Instala automáticamente estas herramientas:

| Herramienta | Para qué sirve |
|---|---|
| **Docker-in-Docker** | Contenedores dentro del Codespace |
| **GitHub CLI** | Gestionar GitHub desde la terminal |
| **Node.js LTS + NVM** | Ejecutar el frontend React |

Configura VS Code con extensiones:
- `github.copilot` → **GitHub Copilot + Copilot Chat** ⭐
- `ms-python.python` + `pylance` + `debugpy` → Desarrollo Python/Django
- `markdown-lint` → Lint de documentación

Activa la configuración clave:
```json
"chat.agent.enabled": true  // ← Habilita el modo Agent de Copilot
```

Expone los puertos de la aplicación:
```
3000  → Frontend React    (público)
8000  → Backend Django    (público)
27017 → MongoDB           (privado)
```

---

### 📄 `post_create.sh` — Se ejecuta UNA VEZ al crear el Codespace

```bash
# 1. Instala MongoDB 6.0 oficial desde repositorios de MongoDB
# 2. Instala python3-venv para crear entornos virtuales Python
# 3. Copia el mensaje de bienvenida al primer arranque
```

> 💡 **Concepto clave:** `postCreateCommand` se ejecuta **solo la primera vez** que se crea el contenedor.

---

### 📄 `post_start.sh` — Se ejecuta CADA VEZ que arranca el Codespace

Este script hace 3 cosas automáticamente:

**1. Hace públicos los puertos:**
```bash
gh cs ports visibility 8000:public
gh cs ports visibility 3000:public
```

**2. Prepara el directorio de datos de MongoDB:**
```bash
sudo mkdir -p /data/db
sudo chmod 777 /data/db
```

**3. Arranca MongoDB con reintentos automáticos (hasta 3 intentos):**
```
Intento 1 → mongod --dbpath /data/db --fork
  → Espera hasta 15 segundos a que esté listo
  → Verifica por: log del proceso / puerto 27017 / ping con mongosh
Si falla → limpia el proceso y reintenta
```

> 💡 **Concepto clave:** `postStartCommand` garantiza que MongoDB siempre esté corriendo cuando abres el Codespace, sin intervención manual.

---

## 📁 MÓDULO 2: `.github/` — La Lógica del Curso

Esta carpeta contiene **4 subcarpetas** que forman el sistema de aprendizaje guiado.

---

### 📂 `instructions/` — Reglas permanentes para Copilot

Son ficheros Markdown con el prefijo `applyTo:` que **Copilot lee automáticamente** como contexto al generar código. Funcionan como el "manual de estándares" del proyecto.

| Fichero | Alcance (`applyTo`) | Qué define |
|---|---|---|
| `octofit_tracker_setup_project.instructions.md` | `**` (todo el proyecto) | Estructura de directorios, `requirements.txt`, virtual env, MongoDB |
| `octofit_tracker_django_backend.instructions.md` | `octofit-tracker/backend/**` | `settings.py`, serializers, URLs, REST endpoints |
| `octofit_tracker_react_frontend.instructions.md` | `octofit-tracker/frontend/**` | Comandos de Create React App, Bootstrap, React Router |

> 💡 **Concepto clave — Custom Instructions:** Copilot lee estos ficheros automáticamente cuando trabajas en ficheros que coinciden con el patrón `applyTo`. Es como darle a Copilot las "normas del proyecto" sin tener que repetirlas en cada prompt.
>
> En Copilot CLI puedes ver las instrucciones activas con: `/instructions`

---

### 📂 `prompts/` — Tareas reutilizables para Copilot

Son ficheros `.prompt.md` que encapsulan instrucciones complejas y repetibles. En VS Code se invocan con `/nombre-del-prompt` en el chat.

#### `create-django-project.prompt.md`
```yaml
mode: 'agent'
model: GPT-4.1
```
Crea el proyecto Django paso a paso:
1. Activa el entorno virtual (`venv`)
2. Ejecuta `django-admin startproject`
3. Ejecuta `migrate`

#### `init-populate-octofit_db.prompt.md`
```yaml
mode: 'agent'
model: GPT-4.1
```
Configura MongoDB + Django ORM + pobla la BD con datos de prueba (superhéroes de Marvel/DC):
- Colecciones: `users`, `teams`, `activities`, `leaderboard`, `workouts`
- Índice único en campo `email`
- Verificación final con `mongosh`

> 💡 **Concepto clave — Prompt Files:** Permiten crear "comandos personalizados" reutilizables para Copilot. En el **Step 3** del curso, el alumno aprende a **crear su propio prompt file** (`update-octofit-tracker-app.prompt.md`).

---

### 📂 `steps/` — Las lecciones del curso

Son 6 ficheros Markdown que definen el contenido de cada lección. Los workflows los publican automáticamente como **comentarios en un Issue de GitHub** a medida que el alumno avanza.

| Fichero | Lección | Qué aprende el alumno |
|---|---|---|
| `1-preparing.md` | **Hola Copilot Agent Mode** | Crear Codespace, usar Copilot Chat en modo Agent, crear rama `build-octofit-app` |
| `2-application-initial-setup.md` | **Setup inicial** | Estructura de directorios, `requirements.txt`, entorno virtual Python |
| `3-django-project-setup.md` | **Django + MongoDB** | Proyecto Django, base de datos, prompt files propios, poblar BD |
| `4-setup-django-rest-framework.md` | **REST API** | Endpoints, CORS, variable `CODESPACE_NAME`, probar con `curl` |
| `5-setup-frontend-react-framework.md` | **Frontend React** | Componentes, Bootstrap, conectar con backend, estilos CSS |
| `6-copilot-on-github.md` | **Copilot en GitHub** | PR summaries automáticos, Copilot Code Review en Pull Requests |

---

### 📂 `workflows/` — La automatización del curso (GitHub Actions)

Son los **"profesores automáticos"** del curso. Cada workflow verifica el trabajo del alumno y publica la siguiente lección.

| Workflow | Trigger | Verificación | Publica |
|---|---|---|---|
| `0-start-exercise.yml` | Push a `main` | — | Step 1 |
| `1-preparing.yml` | Push a cualquier rama | Existe rama `build-octofit-app` | Step 2 |
| `2-application-initial-setup.yml` | Push a `build-octofit-app` | `requirements.txt` contiene `Django==4.1` | Step 3 |
| `3-database-django-project-setup.yml` | Push a `build-octofit-app` | `settings.py` y `populate_db.py` creados | Step 4 |
| `4-setup-django-rest-framework.yml` | Push a `build-octofit-app` | `settings.py` y `views.py` actualizados | Step 5 |
| `5-setup-frontend-react-framework.yml` | Push a `build-octofit-app` | Los 5 componentes React tienen la URL correcta | Step 6 |
| `6-copilot-on-github.yml` | PR mergeado a `main` | Merge completado | 🎉 Fin |

> 💡 **Concepto clave:** El curso es **auto-evaluado**. Un bot llamado "Mona" (via GitHub Actions) comprueba tu código automáticamente en cada `push` y te dice si puedes pasar al siguiente paso.

---

## 🗺️ Flujo Completo del Aprendizaje

```
Alumno hace fork/copy del repositorio
          │
          ▼
    [GitHub Actions] Workflow 0
    Crea un Issue con el Step 1
          │
          ▼
    Alumno abre GitHub Codespace
    ┌─ post_create.sh  → Instala MongoDB + python3-venv (1 vez)
    └─ post_start.sh   → Arranca MongoDB + expone puertos (siempre)
          │
          ▼
    Alumno usa Copilot Agent Mode en VS Code
    con los prompts guiados de cada Step
          │
          ▼
    Alumno hace commit + push
          │
          ▼
    [GitHub Actions] verifica el código automáticamente
          │
     ┌────┴────┐
     │ ¿OK?   │
     │  SÍ    │→ Mona publica el siguiente Step en el Issue
     │  NO    │→ Mona indica el error → alumno corrige y vuelve a push
     └─────────┘
          │
          ▼
    ... (Steps 1 → 6 en bucle) ...
          │
          ▼
    Step 6: Alumno crea Pull Request
    ├── (Opcional) Copilot genera el resumen del PR automáticamente
    └── (Opcional) Copilot hace Code Review del PR
          │
          ▼
    Alumno hace merge → Curso completado 🏆
```

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología | Puerto |
|---|---|---|
| **Frontend** | React.js + Bootstrap + React Router | 3000 (público) |
| **Backend** | Python 3 + Django 4.1 + Django REST Framework | 8000 (público) |
| **Base de datos** | MongoDB 6.0 + Djongo (ORM bridge) | 27017 (privado) |
| **Entorno** | GitHub Codespaces (Ubuntu 22.04) | — |
| **IA** | GitHub Copilot Agent Mode (VS Code) + Copilot CLI | — |

---

## 📖 Referencias

- [GitHub Copilot Agent Mode — Documentación oficial](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)
- [GitHub Copilot CLI — Documentación oficial](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- [Prompt Files en VS Code](https://code.visualstudio.com/docs/copilot/customization/overview#_prompt-files)
- [Custom Instructions en VS Code](https://code.visualstudio.com/docs/copilot/customization/overview#_custom-instructions)
- [Modelos de IA disponibles en GitHub Copilot](https://docs.github.com/en/copilot/reference/ai-models/supported-models)
- [Ingeniería de prompts con GitHub Copilot](https://docs.github.com/en/copilot/concepts/prompt-engineering)
