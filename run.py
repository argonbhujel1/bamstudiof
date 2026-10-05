#!/usr/bin/env python3
"""BAM Studio application entry point (WSGI for Vercel / local)."""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from dotenv import load_dotenv
load_dotenv(os.path.join(ROOT, ".env"))

from app import create_app, db

# Flask WSGI application — name MUST be `app` for Vercel (`run:app`)
app = create_app(os.environ.get("FLASK_ENV", "development"))

# Alias used by some hosts
application = app


def _register_cli():
    """Register Flask CLI commands (local use only)."""
    from app.services.seed import run_seed

    @app.cli.command("seed")
    def seed_command():
        """Seed database with initial data."""
        run_seed()

    @app.cli.command("init-db")
    def init_db():
        """Create all tables and seed."""
        db.create_all()
        run_seed()
        print("Database initialized.")


# Only register CLI when the Flask CLI group exists (skip if stripped)
try:
    if getattr(app, "cli", None) is not None:
        _register_cli()
except Exception:
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
