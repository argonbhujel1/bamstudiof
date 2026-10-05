"""Vercel Python serverless entrypoint.

Exposes a WSGI-compatible Flask application as `app`.
"""
import os
import sys

# Project root (parent of api/)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from dotenv import load_dotenv
load_dotenv(os.path.join(ROOT, ".env"))

from app import create_app

# Production default on Vercel
_config = os.environ.get("FLASK_ENV") or ("production" if os.environ.get("VERCEL") else "development")
app = create_app(_config)

# Explicit WSGI alias (some runtimes look for `application`)
application = app
