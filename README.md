# GH-300 GitHub Copilot Certification — Repositorio de estudio

Repositorio integral para preparar la certificación **GH-300 (GitHub Copilot)** con práctica teórica, ejercicios guiados y proyecto full-stack asistido con Copilot.

---

## 📁 Estructura real del repositorio

```
GH300_GithubCopilot_certification/
├── config-copilot-projects/                  # Plantilla profesional de .github/ (CI/CD, templates, CODEOWNERS)
├── copilot-tests/                            # Simulacros de examen GH-300 + generador de reportes
├── GitHub Copilot Fundamentals/
│   ├── Part 1/
│   │   ├── pj1-intro/                        # Getting Started with GitHub Copilot
│   │   ├── pj2-introduction-to-git-main/     # Introduction to Git
│   │   └── pj3-AccelerateDevGHCopilot/       # Library App (.NET, arquitectura limpia)
│   └── Part 2/
│       └── octofit-tracker/                  # Proyecto práctico Django + React + MongoDB
└── README.md
```

---

## 🎯 Objetivo de cada bloque

### 1) `copilot-tests/` — Simulación de examen (teoría)
- 2 tests completos (`copilot_test_1_questions.md`, `copilot_test_2_questions.md`)
- Preguntas single/multi-select alineadas a dominios GH-300
- Corrección automática por dominio con `generate_report.py`
- Explicaciones completas en `copilot-tests/docs/`

**Uso rápido:**
```bash
python copilot-tests/generate_report.py 1
python copilot-tests/generate_report.py 2
```

> El reporte se genera dentro de `copilot-tests/` como `copilot_test_1_report.md` o `copilot_test_2_report.md`.

Más detalle: [copilot-tests/README.md](copilot-tests/README.md)

### 2) `config-copilot-projects/` — Acelerador de configuración `.github/`
- Scripts para generar estructura profesional de GitHub Actions y governance.
- Incluye workflows de CI, matrix, checks de PR, templates de issue/PR y `CODEOWNERS`.
- Script principal: `config-copilot-projects/scripts/setup-github-structure.sh`

Más detalle: [config-copilot-projects/README.md](config-copilot-projects/README.md)

### 3) `GitHub Copilot Fundamentals/Part 1/` — Laboratorios base
- `pj1-intro`: introducción práctica a GitHub Copilot.
- `pj2-introduction-to-git-main`: fundamentos de Git para flujo de trabajo diario.
- `pj3-AccelerateDevGHCopilot`: aplicación de biblioteca en .NET (dominio, infraestructura, consola, tests).

### 4) `GitHub Copilot Fundamentals/Part 2/octofit-tracker/` — Proyecto práctico GH-300
- Backend: Django + Django REST Framework + MongoDB (djongo)
- Frontend: React + Bootstrap + `HashRouter`
- Material para Agent Mode en `.github/prompts/`, `.github/steps/` e `.github/instructions/`

Más detalle: [GitHub Copilot Fundamentals/Part 2/octofit-tracker/README.md](GitHub%20Copilot%20Fundamentals/Part%202/octofit-tracker/README.md)

---

## 🚀 Ruta recomendada de estudio (GH-300)

1. Realiza `copilot_test_1_questions.md` (100 minutos)
2. Genera reporte y estudia errores por dominio
3. Completa `octofit-tracker` con Copilot Agent Mode
4. Refuerza fundamentos con proyectos de `Part 1`
5. Realiza `copilot_test_2_questions.md` (100 minutos)
6. Compara resultados antes del examen real

---

## ✅ Requisitos sugeridos

- **General**: Git, VS Code, cuenta GitHub
- **Python**: 3.10+ (para scripts/tests/backend Django)
- **Node.js**: 18+ (frontend React)
- **.NET SDK**: para `pj3-AccelerateDevGHCopilot`
- **MongoDB**: requerido para `octofit-tracker/backend`

---

## 🔗 Recursos útiles

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [GH-300 Exam Study Guide](https://examregistration.github.com/certification/GH-300)
- [GitHub Copilot Agent Mode](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React](https://react.dev/)

---

Licencias: revisa los archivos `LICENSE` disponibles en cada módulo/proyecto.
