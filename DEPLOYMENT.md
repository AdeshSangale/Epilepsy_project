Automatic deployment

This repository includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that will attempt to deploy automatically on pushes to `main`.

Supported automatic targets (one or the other, depending on secrets you set):

- Heroku: set the repository Secret `HEROKU_API_KEY`, `HEROKU_APP_NAME`, and optionally `HEROKU_EMAIL`. The workflow uses these to push the application to Heroku.
- Render: set the repository Secret `RENDER_API_KEY` and `RENDER_SERVICE_ID`. The workflow will trigger a deploy for the specified Render service.

To enable automatic deploys via GitHub Actions:

1. In your GitHub repository, go to Settings → Secrets and variables → Actions → New repository secret.
2. Add the secrets required for your provider (see above).
3. Push to the `main` branch — the workflow will run and deploy when the matching secrets are present.

How the workflow behaves

- It runs `manage.py check` and `collectstatic` before attempting deployment.
- If `HEROKU_API_KEY` and `HEROKU_APP_NAME` are present, the workflow uses `akhileshns/heroku-deploy` to deploy.
- If `RENDER_API_KEY` and `RENDER_SERVICE_ID` are present, the workflow posts to the Render API to trigger a deploy.

If you'd like me to fully automate creating a Heroku app or a Render service and set the secrets for you, I can do that — but I will need the corresponding API key (or permission to run the provider's CLI while you authenticate).
