# config-copilot-projects

Plantilla reutilizable para generar una estructura profesional de `.github/` en proyectos nuevos o existentes.

Incluye workflows de CI/CD, validaciones de PR, plantillas de issue, plantilla de pull request y `CODEOWNERS`, con foco en buenas prácticas de desarrollo asistido con GitHub Copilot.

---

## Qué resuelve

- Estandariza calidad y seguridad en repositorios nuevos.
- Reduce tiempo de configuración inicial de GitHub Actions.
- Proporciona una base de validación para código generado con IA.
- Facilita gobernanza (propietarios de código, reglas de PR, convenciones).

---

## Estructura

```
config-copilot-projects/
├── scripts/
│   ├── setup-github-structure.sh
│   └── gen_github.py
└── README.md
```

> Los archivos `.github/` se generan en el proyecto destino al ejecutar el script.

---

## Uso rápido

1. Copia los scripts al repositorio destino:

```bash
cp scripts/setup-github-structure.sh /ruta/proyecto/scripts/
cp scripts/gen_github.py /ruta/proyecto/scripts/
```

2. Ejecuta el generador:

```bash
cd /ruta/proyecto
bash scripts/setup-github-structure.sh
```

3. Variantes comunes:

```bash
bash scripts/setup-github-structure.sh --lang node --coverage 90
bash scripts/setup-github-structure.sh --lang java --coverage 75
bash scripts/setup-github-structure.sh --help
```

---

## Qué se genera en `.github/`

- `workflows/ci.yml`: lint + dead code + security en paralelo y tests con cobertura.
- `workflows/matrix.yml`: pruebas en múltiples versiones del runtime.
- `workflows/pr-checks.yml`: validación de título, tamaño de ficheros y secrets scan.
- `workflows/generate-tests.yml`: scaffold de tests manual vía `workflow_dispatch`.
- `ISSUE_TEMPLATE/`: plantillas de bug y feature request.
- `PULL_REQUEST_TEMPLATE.md`: checklist de calidad en PR.
- `CODEOWNERS`: ownership de revisión por rutas.

---

## Herramientas por lenguaje

| Lenguaje | Lint | Dead Code | Seguridad | Tests |
|---|---|---|---|---|
| Python | flake8 | vulture | bandit | pytest + coverage |
| Node | ESLint | ts-unused-exports | npm audit | Jest |
| Java | Checkstyle | PMD | OWASP Dependency Check | JUnit + JaCoCo |

---

## Requisitos

- Python 3.8+
- Bash
- Git
- Repositorio en GitHub con Actions habilitado

---

## Integración con GH-300

Este módulo está alineado con competencias clave del examen:

- Uso responsable de IA con salvaguardas automáticas de calidad.
- Flujo Copilot + CI/CD para validar cambios rápidamente.
- Dominio práctico de GitHub Actions (matrices, concurrencia, disparadores manuales).
- Estandarización de colaboración con Conventional Commits y `CODEOWNERS`.

---

## Recomendación operativa

Tras generar la estructura:

1. Ajusta `CODEOWNERS` a tu organización.
2. Revisa rutas de código/tests según tu proyecto.
3. Lanza un PR de prueba para validar que todos los checks ejecutan correctamente.
