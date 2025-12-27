# OptiTask AI

Lightweight project that combines a Flask backend, a simple frontend, and an ML engine.

Contents
- `backend/` - Flask app
- `frontend/` - static site and assets
- `ml_engine/` - ML code and requirements
- `docs/PROJECT_REPORT.md` - project report and details

Project structure
- `backend/app.py` - Flask application entrypoint and API routes
- `frontend/index.html` - Minimal frontend UI
- `frontend/assets/logo.png` - Project logo used by frontend
- `ml_engine/engine.py` - Machine learning model logic and inference code
- `ml_engine/requirements.txt` - Python dependencies for ML engine
- `scripts/init_db.sql` - SQL script to initialize the project database
- `.github/workflows/python-ci.yml` - GitHub Actions workflow for CI

Notes
- Virtual environments (`.venv`, `ml_engine/venv`) are intentionally excluded from the repository via `.gitignore`.
- If you want to include additional files, let me know which ones to commit.

Quick start
```powershell
cd "C:\Users\Administrator\Desktop\OptiTask AI"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r ml_engine/requirements.txt
python backend/app.py
```

Contributing
- Open an issue or submit a PR.

License
This project is licensed under the MIT License. See `LICENSE` for details.
