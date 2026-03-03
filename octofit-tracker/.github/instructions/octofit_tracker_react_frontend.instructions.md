---
applyTo: "frontend/**"
---
# Octofit-tracker Fitness App React frontend Guidelines

## REACT Frontend App structure

Make sure in all commands we point to the `frontend` directory

```bash
npx create-react-app frontend --template cra-template --use-npm

npm install bootstrap --prefix frontend

# Add the Bootstrap CSS import at the very top of src/index.js:
sed -i "1iimport 'bootstrap/dist/css/bootstrap.min.css';" frontend/src/index.js

npm install react-router-dom --prefix frontend

```

## Images for the OctoFit Tracker App

The image to use for the app is in the root of this repository docs/octofitapp-small.png
