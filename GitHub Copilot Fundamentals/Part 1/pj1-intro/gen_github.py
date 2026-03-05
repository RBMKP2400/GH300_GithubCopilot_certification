#!/usr/bin/env python3
"""
Generador de estructura .github/ profesional para proyectos de software.
Se invoca desde setup-github-structure.sh
"""
import os
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Genera estructura .github/")
    parser.add_argument("--lang", choices=["python","node","java"], default="python")
    parser.add_argument("--coverage", type=int, default=80)
    return parser.parse_args()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"\033[32m[OK]\033[0m  Creado: {path}")

def get_config(lang, coverage):
    configs = {
        "python": {
            "setup": '      - uses: actions/setup-python@v5\n        with:\n          python-version: "3.11"\n          cache: "pip"',
            "lint_install": "pip install flake8 flake8-bugbear",
            "lint_run": "flake8 src/ tests/ --max-line-length=88 --statistics --count",
            "dead_name": "Dead Code (vulture)",
            "dead_install": "pip install vulture",
            "dead_run": "vulture src/ --min-confidence 80",
            "sec_install": "pip install bandit",
            "sec_run": "bandit -r src/ -ll --exit-zero",
            "test_install": "pip install pytest pytest-cov coverage",
            "test_run": f"pytest tests/ --cov=src --cov-report=term-missing --cov-report=html:coverage-report --cov-report=xml:coverage.xml --cov-fail-under={coverage} -v",
            "matrix_key": "python-version",
            "matrix_vals": '["3.9", "3.10", "3.11", "3.12"]',
            "matrix_setup": '      - uses: actions/setup-python@v5\n        with:\n          python-version: ${{ matrix.python-version }}\n          cache: "pip"',
            "matrix_run": "pip install pytest && pytest tests/ -v",
        },
        "node": {
            "setup": '      - uses: actions/setup-node@v4\n        with:\n          node-version: "20"\n          cache: "npm"',
            "lint_install": "npm ci",
            "lint_run": "npx eslint src/ --max-warnings=0",
            "dead_name": "Unused Exports",
            "dead_install": "npm ci",
            "dead_run": "npx ts-unused-exports tsconfig.json || true",
            "sec_install": "npm ci",
            "sec_run": "npm audit --audit-level=high",
            "test_install": "npm ci",
            "test_run": f"npx jest --coverage --coverageThreshold='{{\"global\":{{\"lines\":{coverage}}}}}'",
            "matrix_key": "node-version",
            "matrix_vals": '["18", "20", "22"]',
            "matrix_setup": '      - uses: actions/setup-node@v4\n        with:\n          node-version: ${{ matrix.node-version }}\n          cache: "npm"',
            "matrix_run": "npm ci && npx jest",
        },
        "java": {
            "setup": '      - uses: actions/setup-java@v4\n        with:\n          java-version: "17"\n          distribution: "temurin"',
            "lint_install": 'echo "Checkstyle via Maven"',
            "lint_run": "mvn checkstyle:check -q",
            "dead_name": "Dead Code (PMD)",
            "dead_install": 'echo "PMD via Maven"',
            "dead_run": "mvn pmd:check -q",
            "sec_install": 'echo "OWASP via Maven"',
            "sec_run": "mvn dependency-check:check -q",
            "test_install": 'echo "JUnit + JaCoCo via Maven"',
            "test_run": "mvn test jacoco:report",
            "matrix_key": "java-version",
            "matrix_vals": '["11", "17", "21"]',
            "matrix_setup": '      - uses: actions/setup-java@v4\n        with:\n          java-version: ${{ matrix.java-version }}\n          distribution: "temurin"',
            "matrix_run": "mvn test -q",
        },
    }
    return configs[lang]

def gen_ci(c, coverage):
    return f"""\
name: CI Pipeline

on:
  push:
    branches: [main, develop, 'feature/**', 'fix/**']
  pull_request:
    branches: [main, develop]

# Cancela runs anteriores del mismo PR para ahorrar minutos de Actions
concurrency:
  group: ci-${{{{ github.workflow }}}}-${{{{ github.ref }}}}
  cancel-in-progress: true

jobs:

  # ─────────────────────────────────────────────────────────────
  # JOB 1 (PARALELO): Linting — estilo y errores de sintaxis
  # ─────────────────────────────────────────────────────────────
  lint:
    name: "Lint"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
{c['setup']}
      - name: Install linter
        run: {c['lint_install']}
      - name: Run linter
        run: {c['lint_run']}

  # ─────────────────────────────────────────────────────────────
  # JOB 2 (PARALELO): Codigo muerto / imports sin usar
  # ─────────────────────────────────────────────────────────────
  dead-code:
    name: "{c['dead_name']}"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
{c['setup']}
      - name: Install tool
        run: {c['dead_install']}
      - name: Run dead code check
        run: {c['dead_run']}

  # ─────────────────────────────────────────────────────────────
  # JOB 3 (PARALELO): Seguridad — vulnerabilidades conocidas
  # ─────────────────────────────────────────────────────────────
  security:
    name: "Security Scan"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
{c['setup']}
      - name: Install security tool
        run: {c['sec_install']}
      - name: Run security scan
        run: {c['sec_run']}

  # ─────────────────────────────────────────────────────────────
  # JOB 4 (SECUENCIAL): Tests + Coverage
  # Usa 'needs' para esperar que los 3 jobs anteriores pasen
  # Si alguno falla, este job NO se ejecuta (ahorra tiempo y minutos)
  # ─────────────────────────────────────────────────────────────
  test:
    name: "Tests + Coverage (>= {coverage}%)"
    runs-on: ubuntu-latest
    needs: [lint, dead-code, security]
    steps:
      - uses: actions/checkout@v4
{c['setup']}
      - name: Install test dependencies
        run: {c['test_install']}
      - name: Run tests with coverage
        run: {c['test_run']}
      - name: Upload coverage report (HTML)
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: coverage-html-report
          path: coverage-report/
          retention-days: 7
      - name: Upload coverage report (XML)
        uses: actions/upload-artifact@v4
        if: success()
        with:
          name: coverage-xml
          path: coverage.xml
          retention-days: 1
"""

def gen_matrix(c):
    return f"""\
name: Matrix Tests

# Prueba en multiples versiones del lenguaje en PARALELO
# fail-fast: false => si una version falla, las demas continuan
on:
  push:
    branches: [main]
  workflow_dispatch:

concurrency:
  group: matrix-${{{{ github.ref }}}}
  cancel-in-progress: true

jobs:
  test-matrix:
    name: "Test / ${{{{ matrix.{c['matrix_key']} }}}}"
    runs-on: ubuntu-latest
    strategy:
      matrix:
        {c['matrix_key']}: {c['matrix_vals']}
      fail-fast: false
    steps:
      - uses: actions/checkout@v4
{c['matrix_setup']}
      - name: Run tests
        run: {c['matrix_run']}
"""

def gen_pr_checks():
    return """\
name: PR Checks

on:
  pull_request:
    branches: [main, develop]

jobs:

  # Verifica que el titulo del PR siga Conventional Commits
  # feat, fix, docs, refactor, test, chore, ci, style
  pr-title:
    name: "PR Title (Conventional Commits)"
    runs-on: ubuntu-latest
    steps:
      - uses: amannn/action-semantic-pull-request@v5
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          types: |
            feat
            fix
            docs
            style
            refactor
            test
            chore
            ci
          requireScope: false

  # Detecta archivos grandes incluidos accidentalmente (> 5MB)
  file-size:
    name: "File Size Check (max 5MB)"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check for large files
        run: |
          MAX_BYTES=$((5 * 1024 * 1024))
          LARGE=$(find . -not -path "./.git/*" -size +${MAX_BYTES}c 2>/dev/null || true)
          if [ -n "$LARGE" ]; then
            echo "Archivos > 5MB encontrados:"
            echo "$LARGE"
            exit 1
          fi
          echo "Sin archivos grandes. OK"

  # Escanea secretos hardcodeados en el diff del PR
  secrets-scan:
    name: "Secrets Scan (TruffleHog)"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.pull_request.base.sha }}
          head: ${{ github.event.pull_request.head.sha }}
          extra_args: --only-verified
"""

def gen_generate_tests(c):
    return f"""\
name: Generate Tests (Manual)

# Se lanza manualmente: GitHub > Actions > Generate Tests > Run workflow
# Genera un scaffold de tests y opcionalmente abre un PR
on:
  workflow_dispatch:
    inputs:
      target_file:
        description: "Archivo a testear (ruta relativa, ej: src/app.py)"
        required: true
        default: "src/app.py"
      open_pr:
        description: "Abrir PR automatico con el scaffold generado?"
        type: boolean
        default: false

jobs:
  generate:
    name: "Scaffold unit tests"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
{c['setup']}
      - name: Install dependencies
        run: {c['test_install']}

      - name: Generate test scaffold
        run: |
          FILE="${{{{ github.event.inputs.target_file }}}}"
          echo "Archivo objetivo: $FILE"
          echo ""
          echo "Usa GitHub Copilot para completar los tests:"
          echo "  1. Abre el archivo fuente en VS Code"
          echo "  2. Abre Copilot Chat (icono superior)"
          echo "  3. Selecciona el codigo y escribe: /tests"
          echo "  4. Revisa los tests generados antes de aceptar"

      - name: Open PR with scaffold
        if: ${{{{ github.event.inputs.open_pr == 'true' }}}}
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          BRANCH="auto/tests-$(date +%Y%m%d%H%M%S)"
          git checkout -b "$BRANCH"
          git add tests/ 2>/dev/null || true
          git diff --cached --quiet && echo "Nada nuevo que commitear" && exit 0
          git commit -m "test: scaffold for ${{{{ github.event.inputs.target_file }}}}"
          git push origin "$BRANCH"
          PR_BODY=$(printf 'Tests generados automaticamente via workflow.\\n\\nPasos siguientes:\\n- Abrir en VS Code y usar Copilot Chat con /tests\\n- Revisar y completar los casos de prueba\\n- Verificar que pasan localmente antes de mergear')
          gh pr create \\
            --title "test: scaffold for ${{{{ github.event.inputs.target_file }}}}" \\
            --body "$PR_BODY" \\
            --base main
        env:
          GH_TOKEN: ${{{{ secrets.GITHUB_TOKEN }}}}
"""

def gen_pr_template(coverage):
    return f"""\
## Descripcion

<!-- Explica brevemente que cambia este PR y por que -->

## Tipo de cambio

- [ ] `feat`: nueva funcionalidad
- [ ] `fix`: correccion de bug
- [ ] `refactor`: cambio sin nueva funcionalidad ni fix
- [ ] `test`: tests nuevos o modificados
- [ ] `docs`: solo documentacion
- [ ] `ci`: cambios en workflows o CI/CD
- [ ] `chore`: mantenimiento (dependencias, build)

## Checklist

- [ ] El codigo pasa el linter sin warnings
- [ ] Se han anadido tests para los cambios
- [ ] Todos los tests pasan localmente
- [ ] La cobertura no baja del {coverage}%
- [ ] Sin secretos ni credenciales hardcodeadas
- [ ] Documentacion actualizada si corresponde

## Como probar

```bash
# Comandos para verificar localmente:

```

## Issues relacionados

Closes #
"""

def gen_bug_report():
    return """\
name: Bug Report
description: Reportar un comportamiento incorrecto
labels: ["bug", "triage"]

body:
  - type: markdown
    attributes:
      value: "Gracias por reportar un bug. Rellena todos los campos para ayudarnos a reproducirlo."

  - type: textarea
    id: description
    attributes:
      label: Descripcion del bug
      placeholder: "Al hacer X ocurre Y, pero deberia ocurrir Z"
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Pasos para reproducir
      value: |
        1.
        2.
        3.
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Comportamiento esperado
    validations:
      required: true

  - type: textarea
    id: environment
    attributes:
      label: Entorno
      value: |
        - OS:
        - Version del proyecto:
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Logs o stack trace
      render: shell
"""

def gen_feature_request():
    return """\
name: Feature Request
description: Proponer una nueva funcionalidad
labels: ["enhancement"]

body:
  - type: textarea
    id: problem
    attributes:
      label: Problema que resuelve
      placeholder: "Me frustra cuando..."
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Solucion propuesta
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternativas consideradas

  - type: textarea
    id: context
    attributes:
      label: Contexto adicional
"""

def gen_codeowners():
    return """\
# CODEOWNERS — Define quien debe revisar cada parte del codigo
# Formato: <patron>  <@usuario o @org/equipo>
# Docs: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners

# Propietario por defecto (todo el repositorio)
*                   @tu-usuario

# Workflows CI/CD — requiere revision del equipo DevOps
.github/workflows/  @tu-usuario

# Tests — cualquier cambio requiere revision
tests/              @tu-usuario
"""

def main():
    args = parse_args()
    lang = args.lang
    coverage = args.coverage
    base = ".github"

    if os.path.isdir(base):
        resp = input(f"\033[33m[WARN]\033[0m La carpeta .github/ ya existe. Sobreescribir? (s/N): ")
        if resp.lower() != "s":
            print("Operacion cancelada.")
            sys.exit(0)

    print(f"\033[36m[INFO]\033[0m Generando .github/ para proyecto {lang} (coverage >= {coverage}%)\n")

    c = get_config(lang, coverage)

    write_file(f"{base}/workflows/ci.yml",             gen_ci(c, coverage))
    write_file(f"{base}/workflows/matrix.yml",          gen_matrix(c))
    write_file(f"{base}/workflows/pr-checks.yml",       gen_pr_checks())
    write_file(f"{base}/workflows/generate-tests.yml",  gen_generate_tests(c))
    write_file(f"{base}/PULL_REQUEST_TEMPLATE.md",      gen_pr_template(coverage))
    write_file(f"{base}/ISSUE_TEMPLATE/bug_report.yml", gen_bug_report())
    write_file(f"{base}/ISSUE_TEMPLATE/feature_request.yml", gen_feature_request())
    write_file(f"{base}/ISSUE_TEMPLATE/config.yml",     "blank_issues_enabled: false\n")
    write_file(f"{base}/CODEOWNERS",                    gen_codeowners())

    # Forzar UTF-8 en stdout para Windows (evita UnicodeEncodeError en cp1252)
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    sep = "=" * 56
    print(f"\n{sep}")
    print(f"  Estructura .github/ generada con exito")
    print(f"{sep}\n")
    print(f"  Lenguaje  : {lang}")
    print(f"  Coverage  : >= {coverage}%\n")
    print("  Archivos creados:")

    for root, dirs, files in os.walk(base):
        dirs.sort()
        for fname in sorted(files):
            fpath = os.path.join(root, fname).replace("\\", "/")
            print(f"    + {fpath}")

    print(f"""
  Proximos pasos:
  1. Edita .github/CODEOWNERS con tu usuario de GitHub
  2. Ajusta las rutas src/ y tests/ si tu proyecto las tiene distintas
  3. Haz commit:
       git add .github && git commit -m 'ci: add github structure'
  4. Haz push y revisa la pestana Actions en GitHub

  Tip GH-300: Abre cualquier .yml en VS Code y usa
  Copilot Chat con /explain para entender cada seccion.
""")

if __name__ == "__main__":
    main()
