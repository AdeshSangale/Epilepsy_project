# Epilepsy_project

Epilepsy seizure detection web application built with Django.

Contents

- Django project and app code
- Static assets and templates
- Datasets (raw EEG text files) — these are included in the repository currently; consider moving large datasets elsewhere or using Git LFS.

Quick start

1. Create and activate a Python virtual environment:

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```
python -m pip install -r requirements.txt
```

3. Run the server:

```
python manage.py migrate
python manage.py runserver
```

Notes

- `db.sqlite3` and `model.joblib` are intentionally excluded via `.gitignore`.
- If you want large datasets removed from history or tracked with Git LFS, open an issue or ask me to help.
