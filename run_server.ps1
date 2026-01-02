<#
run_server.ps1 - Cross-platform PowerShell helper to create venv (if needed), install dev deps,
run migrations and start Django dev server, then open http://127.0.0.1:8000/ in default browser.

Double-click or run in PowerShell: .\run_server.ps1
#>
Set-Location -Path $PSScriptRoot

if (-not (Test-Path -Path .venv)) {
    Write-Host "Creating virtual environment .venv..."
    python -m venv .venv
}

Write-Host "Activating virtual environment..."
if (Test-Path ".venv\Scripts\Activate.ps1") {
    . .\.venv\Scripts\Activate.ps1
} else {
    Write-Warning "PowerShell activation script not found; ensure .venv exists and use your preferred activation method. Proceeding with 'python' on PATH."
}

Write-Host "Upgrading pip and installing development requirements..."
python -m pip install --upgrade pip
if (Test-Path "requirements-dev.txt") {
    python -m pip install -r requirements-dev.txt
}

Write-Host "Applying migrations..."
python manage.py migrate

Write-Host "Starting Django development server in new window..."
Start-Process -FilePath powershell -ArgumentList "-NoExit","-Command","python manage.py runserver"

Start-Sleep -Seconds 3
Start-Process "http://127.0.0.1:8000/"

Write-Host "Done. Close the server window to stop the development server."
