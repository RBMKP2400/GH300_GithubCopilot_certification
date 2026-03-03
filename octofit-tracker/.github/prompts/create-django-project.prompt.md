---
mode: 'agent'
model: GPT-4.1
description: 'Create a Django project, start it, and run it'
---

Your task is to create the Django project in backend/src directory using the Python
virtual environment we already created in directory backend/venv which contains all the prerequisites.


To create the Django project follow these steps.
1. Make sure we are in the root directory and don't change directories
2. source backend/venv/bin/activate
3. django-admin startproject src in the backend directory
4. python manage.py migrate
5. Instruct the user to run the django app from the .vscode/launch.json configuration that is in the repository
