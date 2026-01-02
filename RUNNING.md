# Running the project (local)

This file documents the cross-platform run/setup helpers added to the repository.

Files added

- `run_server.bat` - Windows batch file (double-click) that activates `.venv` if present and starts the Django dev server, then opens the browser.
- `run_server.ps1` - PowerShell script: creates `.venv` if missing, activates it, installs `requirements-dev.txt`, runs migrations, starts the server in a new window and opens the browser.
- `run_server.sh` - POSIX shell script (Linux / macOS / WSL): creates `.venv` if missing, activates it, installs `requirements-dev.txt`, runs migrations, starts server, and opens browser.

Quick usage

PowerShell (recommended on Windows):

```
cd \path\to\Epilepsy_project
./run_server.ps1
```

Double-click in Explorer (Windows):

- Double-click `run_server.bat` in the project root.

Linux / macOS / WSL:

```
cd /path/to/Epilepsy_project
chmod +x run_server.sh
./run_server.sh
```

Notes

- For local development, use `requirements-dev.txt` which excludes platform-specific production packages.
- If you prefer to manage dependencies manually: create a venv and install `requirements-dev.txt`.
- If you want a Docker-based setup for deterministic builds across environments, I can add a Dockerfile and docker-compose.
