# PoC: Orquestación de Agentes con Validación Local (Simulando CI)

Esta guía describe un flujo de trabajo 100% local que simula el desarrollo en paralelo y la integración continua. El objetivo es validar el trabajo de los agentes a nivel local antes de considerar cualquier interacción con un repositorio remoto.

## Ruta Rápida (Dos Terminales + Integración)

Hay **dos scripts** en este proyecto:

| Script | Para qué sirve |
|---|---|
| `setup-agent-worktrees.ps1` | Crea dos working directories aislados para que `feature/agent-1` y `feature/agent-2` no se pisen. |
| `run-vibe-integration.ps1` | Tú desarrollas en Copilot interactivo (2 terminales). El script solo valida y mergea al final. |
---

### Opción A — Tú desarrollas con Copilot, el script integra

#### Paso 0: Preparar entorno (una sola vez)

Abre una terminal PowerShell en la carpeta del proyecto:

```powershell
cd poc-parallel-agents
.venv\Scripts\activate          # activa el entorno virtual
pip install -r requirements.txt # instala flake8, vulture, pytest, bandit
```

---

#### Paso 1: Crear worktrees aislados (evita cambios de rama cruzados)

En la carpeta del repo principal, ejecuta:

```powershell
cd poc-parallel-agents
.\setup-agent-worktrees.ps1 -BaseBranch "feature/poc-parallel-agents" -Agent1Path ".worktrees\agent-1" -Agent2Path ".worktrees\agent-2"
```

Esto crea dos carpetas hermanas:

1. `.worktrees\agent-1` apuntando a `feature/agent-1`
2. `.worktrees\agent-2` apuntando a `feature/agent-2`

Cada carpeta tiene su propio checkout. Si cambias de rama en una, la otra no cambia.

---

#### Paso 2: Terminal A — Agente 1

Abre una terminal nueva (puedes usar `+` en el panel de terminales de VS Code):

```powershell
poc-parallel-agents\.venv\Scripts\activate
cd .worktrees\agent-1\poc-parallel-agents
copilot --yolo
```

Cuando Copilot abra su interfaz de chat, pegas este prompt:

```
Estoy en la rama feature/agent-1 y SOLO puedes tocar archivos de este alcance:
- main.py
- test/*.py

Tu misión:
1. Añade la función `calculate_discount(price, pct)` en main.py que aplique un descuento porcentual y devuelva el precio final.
2. Crea el archivo test/test_discount.py con tests unitarios con pytest que cubran casos normales y edge cases (descuento 0, descuento 100, precio negativo).
3. Asegúrate de que flake8, vulture y bandit no reportan errores.
4. Haz un commit en la rama actual con mensaje: feat: add calculate_discount function
5. No hagas push.
6. No crees scripts auxiliares (.bat/.py/.md) ni toques README.
```
Se recomienda pasar a modo plan y luego a autopilot para ejecutar el plan.

> [!TIP]
> Copilot irá ejecutando pasos. Si te pregunta algo, responde en lenguaje natural.
> Cuando termine, verás el resumen con el hash del commit.
> Puedes seguir iterando: escribe más instrucciones en el mismo chat si quieres ajustar algo.
> Para salir cuando estés satisfecho pulsa **Ctrl+C** o escribe `/exit`.


Espera a que Copilot confirme el commit. Puedes iterar cuanto quieras antes de salir con **Ctrl+C**.

---

#### Paso 3: Terminal B — Agente 2

Abre **otra terminal nueva** (no cierres la anterior):

```powershell
poc-parallel-agents\.venv\Scripts\activate
cd .worktrees\agent-2\poc-parallel-agents
copilot --yolo
```

Prompt para este agente:

```
Estoy en la rama feature/agent-2 y SOLO puedes tocar archivos de este alcance:
- main.py
- test/*.py

Tu misión:
1. Añade la función `apply_tax(price, tax_rate)` en main.py que sume impuestos al precio base y devuelva el total.
2. Crea el archivo test/test_tax.py con tests unitarios con pytest que cubran casos normales y edge cases (tasa 0, tasa 100, precio negativo).
3. Asegúrate de que flake8, vulture y bandit no reportan errores.
4. Haz un commit en la rama actual con mensaje: feat: add apply_tax function
5. No hagas push.
6. No crees scripts auxiliares (.bat/.py/.md) ni toques README.
```
Se recomienda pasar a modo plan y luego a autopilot para ejecutar el plan.

> [!TIP]
> Copilot irá ejecutando pasos. Si te pregunta algo, responde en lenguaje natural.
> Cuando termine, verás el resumen con el hash del commit.
> Puedes seguir iterando: escribe más instrucciones en el mismo chat si quieres ajustar algo.
> Para salir cuando estés satisfecho pulsa **Ctrl+C** o escribe `/exit`.


Espera a que Copilot confirme el commit. Puedes iterar cuanto quieras antes de salir con **Ctrl+C**.

---

#### Paso 4: Integración automática

Con ambas ramas commitadas, abre una tercera terminal (o reutiliza cualquiera):

```powershell
cd poc-parallel-agents
.venv\Scripts\activate
./run-vibe-integration.ps1 -BaseBranch "feature/poc-parallel-agents" -Agent1Branch "feature/agent-1" -Agent2Branch "feature/agent-2"
```

El script hace automaticamente:
1. Valida calidad de `feature/agent-1` (flake8 + vulture + pytest + bandit).
2. Valida calidad de `feature/agent-2` (igual).
3. Fusiona ambas en `feature/poc-parallel-agents`.
4. Si hay conflicto, lanza Copilot para resolverlo.
5. Valida calidad del resultado final.
6. Muestra el historial de commits.

> [!NOTE]
> Si quieres simular el flujo sin ejecutar nada todavía:
> ```powershell
> ./run-vibe-integration.ps1 -DryRun
> ```

---

### Opción B — Flujo completamente manual (sin Copilot CLI)

> [!NOTE]
> Esta opción es para entender el flujo desde cero, sin usar ningún script ni Copilot CLI.
> Tú editas los archivos, ejecutas los comandos de validación y resuelves los conflictos a mano.
> Las Opciones A y B automatizan exactamente este mismo flujo.

## El Flujo de Trabajo Manual (100% Local)

1.  **Setup (Local)**: Se prepara el repositorio local y el entorno de desarrollo.
2.  **Desarrollo (Local)**: Dos agentes trabajan en paralelo en sus propias ramas, creando funcionalidades que entrarán en conflicto.
3.  **Validación (Local, Simulando CI)**: Un agente integrador ejecuta scripts de validación (linting, tests) sobre las ramas de los agentes *antes* de fusionar.
4.  **Integración (Local)**: Solo si la validación es exitosa, el integrador fusiona las ramas en `main` y resuelve los conflictos, todo en el entorno local.

---

## Paso 1: Configuración Inicial (Local)

### 1.1. Preparar el Entorno

Primero, asegúrate de tener Python instalado. Luego, crea un entorno virtual para instalar las herramientas de validación y evitar conflictos con otros proyectos.

> [!IMPORTANT]
> No necesitas definir `PYTHONPATH` para este PoC. Trabajando desde la carpeta `poc-parallel-agents` (dentro de tu workspace `C:\Users\carlos.gonzalez-novo\Desktop\Learning\GH300_GithubCopilot_certification`) es suficiente.

```bash
# Navega al directorio del proyecto
cd poc-parallel-agents

# Crea un entorno virtual
python -m venv .venv

# Activa el entorno virtual
# En Windows (PowerShell/CMD):
.venv\Scripts\activate
# En macOS/Linux (bash):
source .venv/bin/activate

# Instala las herramientas de validación
pip install flake8 vulture pytest bandit
```

### 1.2. Inicializar el Repositorio

Ahora, inicializa el repositorio de Git con el contenido inicial de `main.py`.

### Prompt del Agente Orquestador
"Prepara el entorno de trabajo. En el directorio `poc-parallel-agents`, inicializa un repositorio de Git y realiza el primer commit en la rama `feature/poc-parallel-agents` con el contenido del archivo `main.py`."

### Implementación (Terminal 1: `main-branch`)
```bash
# 1. Inicializa el repositorio
git init

# 2. Añade todos los archivos y crea el primer commit
git add .
git commit -m "Initial commit"
```

---

## Paso 2: Desarrollo de los Agentes (Local)

Dos agentes desarrollarán funcionalidades de forma aislada en sus propias ramas.

### Prompt del Agente 1
"Tu misión es desarrollar la 'funcionalidad A'. Crea una nueva rama `feature/agent-1`, modifica `main.py` para añadir la función `feature_a` y confirma tus cambios. Asegúrate de que tu código sigue las convenciones de estilo de Python."

### Implementación (Terminal 2: `agent-1`)
```bash
# Crea y cambia a la nueva rama
git checkout -b feature/agent-1

# Edita main.py y añade la función feature_a al principio del archivo:
```
```python
def feature_a():
    """Esta es la funcionalidad A."""
    print("Esta es la funcionalidad A.")

# main.py

def initial_function():
# ... (resto del archivo sin cambios)
```
```bash
# Confirma tus cambios
git add main.py
git commit -m "feat: Agente 1 añade la función feature_a"
```

### Prompt del Agente 2
"Tu misión es desarrollar la 'funcionalidad B'. Crea una rama `feature/agent-2` desde `main`, modifica `main.py` para añadir la función `feature_b` (generando un conflicto) y confirma los cambios. Presta atención a la calidad del código."

### Implementación (Terminal 3: `agent-2`)
```bash
# Vuelve a main para empezar desde una base limpia
git checkout main

# Crea y cambia a la nueva rama
git checkout -b feature/agent-2

# Edita main.py y añade la función feature_b al principio del archivo.
# Esto creará un conflicto con el trabajo del Agente 1.
```
```python
def feature_b():
    """Esta es la funcionalidad B."""
    print("Esta es la funcionalidad B.")

# main.py

def initial_function():
# ... (resto del archivo sin cambios)
```
```bash
# Confirma tus cambios
git add main.py
git commit -m "feat: Agente 2 añade la función feature_b"
```

---

## Paso 3: Validación Local (Simulando la CI)

### Prompt del Agente Integrador
"Tu misión es actuar como el guardián de la calidad de la rama `main`. Antes de fusionar cualquier rama, debes validarla. Cambia a cada rama de `feature` y ejecuta los comandos de validación local. Solo si los checks son exitosos, puedes proceder a la fusión."

### ¿Qué son `flake8` y `bandit`?
*   **`flake8`**: Es un "linter" que revisa tu código en busca de errores de estilo (espacios incorrectos, líneas muy largas, etc.) y algunos errores de programación comunes. Ayuda a mantener el código limpio y legible.
*   **`bandit`**: Es un analizador de seguridad que busca vulnerabilidades conocidas en tu código Python.

### Implementación (Terminal 1: `main-branch`)

Ahora, ejecuta la validación para cada rama. Asegúrate de tener el entorno virtual activado.

```bash
# Validar el trabajo del Agente 1
git checkout feature/agent-1
echo "--- Validando rama feature/agent-1 ---"
flake8 main.py
bandit -r main.py

# Validar el trabajo del Agente 2
git checkout feature/agent-2
echo "--- Validando rama feature/agent-2 ---"
flake8 main.py
bandit -r main.py
```
Si ninguno de los comandos anteriores arroja errores, significa que ambas ramas cumplen con los estándares de calidad y están listas para ser integradas.

---

## Paso 4: Integración y Resolución de Conflictos (Local)

### Prompt del Agente Integrador
"Ahora que has validado que ambas ramas cumplen con los estándares de calidad, procede a integrarlas en `main`. Fusiona primero `feature/agent-1`. Luego, fusiona `feature/agent-2`, lo que generará un conflicto. Resuélvelo manualmente, asegurando que ambas funcionalidades coexisten. Finaliza la fusión."

### Implementación (Terminal 1: `main-branch`)
```bash
# 1. Vuelve a la rama principal
git checkout main

# 2. Fusiona la primera rama (sin conflictos)
git merge feature/agent-1

# 3. Fusiona la segunda rama (esto creará un conflicto)
git merge feature/agent-2
```

### ¡Acción Manual Requerida! Resolución del Conflicto

Al ejecutar el último comando, Git te notificará de un conflicto en `main.py`. Si abres el archivo, verás algo así:

```python
<<<<<<< HEAD
def feature_a():
    """Esta es la funcionalidad A."""
    print("Esta es la funcionalidad A.")
=======
def feature_b():
    """Esta es la funcionalidad B."""
    print("Esta es la funcionalidad B.")
>>>>>>> feature/agent-2

# main.py

def initial_function():
# ... (resto del código)
```

*   `<<<<<<< HEAD`: Es el inicio del bloque de código de tu rama actual (`main`).
*   `=======`: Separa los dos bloques en conflicto.
*   `>>>>>>> feature/agent-2`: Es el final del bloque de código de la rama que intentas fusionar.

Para resolverlo, **edita el archivo para que contenga ambas funcionalidades** y elimina los marcadores de conflicto:

```python
def feature_a():
    """Esta es la funcionalidad A."""
    print("Esta es la funcionalidad A.")

def feature_b():
    """Esta es la funcionalidad B."""
    print("Esta es la funcionalidad B.")

# main.py

def initial_function():
    """
    Esta es la función inicial del proyecto.
    Sirve como punto de partida antes de que los agentes comiencen a trabajar.
    """
    print("Proyecto inicial listo.")

if __name__ == "__main__":
    initial_function()
```

### Finalizar la Fusión

Una vez resuelto el conflicto, guarda el archivo y finaliza la fusión.

```bash
# 4. Añade el archivo resuelto y completa el commit de fusión
git add main.py
git commit
```
Git abrirá un editor de texto para que confirmes el mensaje del commit de fusión. Simplemente guarda y cierra el editor.

### Verificación Final
```bash
git log --graph --oneline --all
```
El historial mostrará las dos ramas fusionadas en `main`, todo validado y resuelto en tu entorno local. ¡Felicidades!

