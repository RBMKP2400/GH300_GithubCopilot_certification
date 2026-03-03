# GH-300 GitHub Copilot Certification — Study Repository

<p align="center">
  <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="80" alt="GitHub"/>
</p>

This repository is a **complete preparation toolkit for the GH-300 GitHub Copilot certification exam**.  
It contains two independent modules that together cover both the theoretical and practical sides of the exam.

---

## 📁 Repository Structure

```
GH300_GithubCopilot_certification/
│
├── copilot-tests/          ← 📝 Exam simulation tests (theory)
│   ├── copilot_test_1_questions.md
│   ├── copilot_test_2_questions.md
│   ├── generate_report.py
│   └── README.md           ← Full instructions for taking the tests
│
└── octofit-tracker/        ← 🏋️ Hands-on coding project (practical)
    ├── README.md            ← Full instructions for building the app
    ├── backend/             ← Django REST API + MongoDB
    ├── frontend/            ← React + Bootstrap SPA
    └── .github/
        ├── instructions/    ← Copilot Agent Mode instruction files
        ├── prompts/         ← Reusable prompt files
        ├── steps/           ← Step-by-step guided exercise
        └── workflows/       ← GitHub Actions validation workflows
```

---

## 📝 Module 1 — Exam Simulation Tests (`copilot-tests/`)

Two full-length practice tests that simulate the GH-300 exam format.

**What you get:**
- Questions mapped to the official GH-300 exam domains
- Multi-select and single-select question types
- Automatic grading with domain-by-domain score breakdown
- Detailed explanations for every answer

**Quick start:**
```bash
# 1. Open a question file and mark your answers (change [ ] to [x])
code copilot-tests/copilot_test_1_questions.md

# 2. Generate the graded report
python copilot-tests/generate_report.py 1
```

> 📖 See [`copilot-tests/README.md`](copilot-tests/README.md) for full instructions.

---

## 🏋️ Module 2 — OctoFit Tracker App (`octofit-tracker/`)

A hands-on coding exercise that builds a full fitness tracking application using **GitHub Copilot Agent Mode** — demonstrating the AI-assisted development workflow tested in the GH-300 exam.

**What you build:**

| Layer | Technology | Purpose |
|---|---|---|
| Backend API | Django 4 + Django REST Framework | REST endpoints for users, teams, activities, leaderboard, workouts |
| Database | MongoDB via djongo | NoSQL persistence |
| Frontend | React 19 + Bootstrap 5 | SPA with navigation and data display |

**Two ways to build it:**

### Option A — Automated with GitHub Copilot (recommended for exam practice)
Open a Codespace, then use Copilot Agent Mode with the provided prompt files:
```
.github/prompts/create-django-project.prompt.md
.github/prompts/init-populate-octofit_db.prompt.md
```
Follow the step-by-step guide in [`.github/steps/`](octofit-tracker/.github/steps/).

### Option B — Manual setup
```bash
# Backend
python3 -m venv octofit-tracker/backend/venv
source octofit-tracker/backend/venv/bin/activate
pip install -r octofit-tracker/backend/requirements.txt
cd octofit-tracker/backend
python manage.py migrate && python manage.py populate_db
python manage.py runserver 0.0.0.0:8000

# Frontend (separate terminal)
cd octofit-tracker/frontend
npm install && npm start
```

> 📖 See [`octofit-tracker/README.md`](octofit-tracker/README.md) for the full guide including Codespace-specific setup, port configuration, and troubleshooting.

---

## 🚀 Getting Started

### Prerequisites
- GitHub account with access to Codespaces
- Basic knowledge of Python, JavaScript, and REST APIs

### Recommended workflow

```
1. Read this README
        ↓
2. Take copilot-tests/ exam 1 (100 min timer)
   → Review your score and study weak domains
        ↓
3. Build the octofit-tracker/ app using Copilot Agent Mode
   → Practice AI-assisted development workflows
        ↓
4. Take copilot-tests/ exam 2 (100 min timer)
   → Validate improvement before the real exam
```

### Open in a Codespace
Click the button below to launch a pre-configured dev environment with Python, Node.js, and MongoDB ready to use:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/RBMKP2400/GH300_GithubCopilot_certification)

---

## 📚 GH-300 Exam Domains Covered

| Domain | copilot-tests | octofit-tracker |
|---|:---:|:---:|
| GitHub Copilot fundamentals | ✅ | |
| Copilot in the IDE (code completions, chat) | ✅ | ✅ |
| Copilot Agent Mode & prompt engineering | ✅ | ✅ |
| Copilot on GitHub.com (PR summaries, reviews) | ✅ | |
| Responsible AI / content exclusions / policies | ✅ | |
| GitHub Copilot for business administration | ✅ | |

---

## 🔗 Useful Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [GH-300 Exam Study Guide](https://examregistration.github.com/certification/GH-300)
- [GitHub Copilot Agent Mode](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React Documentation](https://react.dev/)

---

&copy; 2025 GitHub &bull; [MIT License](https://gh.io/mit)
