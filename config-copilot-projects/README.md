# config-copilot-projects

Plantilla de configuracion profesional de `.github/` para cualquier proyecto de desarrollo de software con GitHub Copilot.

Incluye un generador automatizado que crea la estructura completa de CI/CD, templates de Issues y Pull Requests, y CODEOWNERS.

---

## Estructura del repositorio

```
config-copilot-projects/
├── scripts/
│   ├── setup-github-structure.sh   # Punto de entrada (wrapper bash)
│   └── gen_github.py               # Generador Python con toda la logica
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                  # CI principal con paralelizacion
│   │   ├── matrix.yml              # Tests en multiples versiones
│   │   ├── pr-checks.yml           # Validaciones en Pull Requests
│   │   └── generate-tests.yml      # Scaffold de tests (manual)
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   ├── feature_request.yml
│   │   └── config.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── CODEOWNERS
└── README.md
```

---

## Como usar en un proyecto nuevo

### 1. Copia los scripts al proyecto destino

```bash
cp scripts/setup-github-structure.sh /ruta/tu-proyecto/scripts/
cp scripts/gen_github.py             /ruta/tu-proyecto/scripts/
```

### 2. Ejecuta el generador

```bash
cd /ruta/tu-proyecto

# Python — 80% coverage (por defecto)
bash scripts/setup-github-structure.sh

# Node.js — 90% coverage
bash scripts/setup-github-structure.sh --lang node --coverage 90

# Java — 75% coverage
bash scripts/setup-github-structure.sh --lang java --coverage 75

# Ayuda
bash scripts/setup-github-structure.sh --help
```

### 3. Personaliza y haz commit

```bash
# Edita CODEOWNERS con tu usuario de GitHub
# Ajusta rutas src/ y tests/ si tu proyecto las tiene distintas

git add .github
git commit -m "ci: add github structure"
git push
```

---

## Workflows generados

### `ci.yml` — Pipeline CI principal

Ejecuta 3 jobs en **paralelo** y solo lanza los tests si todos pasan:

```
Push / PR
    │
    ├── lint      (paralelo) ─┐
    ├── dead-code (paralelo) ─┼─► test + coverage
    └── security  (paralelo) ─┘
```

Usa `concurrency` para cancelar runs anteriores del mismo PR.

### `matrix.yml` — Tests multi-version

Prueba en multiples versiones del lenguaje simultaneamente con `fail-fast: false`.

| Lenguaje | Versiones |
|---|---|
| Python | 3.9, 3.10, 3.11, 3.12 |
| Node | 18, 20, 22 |
| Java | 11, 17, 21 |

### `pr-checks.yml` — Validaciones en PRs

| Check | Descripcion |
|---|---|
| PR Title | Titulo sigue Conventional Commits (feat, fix, docs...) |
| File Size | Detecta archivos > 5MB incluidos accidentalmente |
| Secrets Scan | Escanea secretos hardcodeados con TruffleHog |

### `generate-tests.yml` — Scaffold de tests (manual)

Se lanza desde `GitHub > Actions > Generate Tests > Run workflow`.
Crea un scaffold de tests y opcionalmente abre un PR automatico.

---

## Herramientas por lenguaje

| Lenguaje | Lint | Dead Code | Security | Tests |
|---|---|---|---|---|
| Python | flake8 | vulture | bandit | pytest + coverage |
| Node | ESLint | ts-unused-exports | npm audit | Jest |
| Java | Checkstyle | PMD | OWASP | JUnit + JaCoCo |

---

## Requisitos

- Python 3.8+
- Git
- Acceso a GitHub Actions (repositorio en GitHub)

---

## Relevancia GH-300 (GitHub Copilot Certification)

Esta estructura implementa las mejores practicas del examen GH-300:

- **Uso responsable de IA**: safety net automatizado (lint, tests, coverage) para validar codigo generado por Copilot
- **Flujo de desarrollo con Copilot**: integracion de Copilot en CI/CD via `generate-tests.yml`
- **GitHub Actions**: paralelizacion, concurrency, matrix strategy, workflow_dispatch
- **Conventional Commits**: estandar de mensajes requerido en el examen
- **CODEOWNERS**: control de revisiones por area del codigo
