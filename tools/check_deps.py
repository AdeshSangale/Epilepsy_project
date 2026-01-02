"""
check_deps.py

Scans Python files in the repository for import statements and attempts
to import each external module to report missing runtime dependencies.

Run this inside your virtual environment (or global Python) as:
    python tools/check_deps.py

The script prints modules that failed to import.
"""
import ast
import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))

def find_py_files(root):
    for dirpath, dirs, files in os.walk(root):
        # Skip virtualenvs and .git
        if any(x in dirpath for x in (".venv", "venv", ".git", "__pycache__")):
            continue
        for f in files:
            if f.endswith(".py"):
                yield os.path.join(dirpath, f)

def extract_imports(path):
    with open(path, "r", encoding="utf-8") as fh:
        try:
            node = ast.parse(fh.read(), filename=path)
        except Exception:
            return set()
    imports = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Import):
            for alias in n.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(n, ast.ImportFrom):
            if n.module:
                imports.add(n.module.split('.')[0])
    return imports

def main():
    print(f"Scanning for imports under {ROOT}...\n")
    all_imports = set()
    for p in find_py_files(ROOT):
        mods = extract_imports(p)
        all_imports.update(mods)

    # Exclude standard library and local packages heuristically
    local_packages = {"Epilepsy_App", "Epilepsy_project"}
    ignore = set(sys.builtin_module_names) | {"os", "sys", "pathlib", "typing", "ast", "json", "re", "datetime", "subprocess", "shutil", "io", "logging", "inspect", "functools", "itertools", "collections", "math", "csv", "http", "threading", "time"}

    candidates = sorted(x for x in all_imports if x and x not in ignore and x not in local_packages)

    missing = []
    for mod in candidates:
        try:
            __import__(mod)
        except Exception as e:
            missing.append((mod, str(e)))

    if not candidates:
        print("No external imports detected.")
        return

    print("Detected import candidates:\n", ", ".join(candidates), "\n")

    if missing:
        print("\nMissing or failing imports:")
        for mod, err in missing:
            print(f" - {mod}: {err}")
        print("\nRecommendation: install missing packages, for example:\n  python -m pip install <package>\nOr use requirements-dev.txt for development dependencies:
  python -m pip install -r requirements-dev.txt")
    else:
        print("\nAll detected imports imported successfully in the current environment.")

if __name__ == '__main__':
    main()
