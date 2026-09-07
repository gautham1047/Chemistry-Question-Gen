import os
import sys

# Vercel places Python functions in /api, but the Flask app and all of its
# modules (src/, chemData.py, data/) live in /backend. Add that directory to
# the import path so `from app import app` and its transitive imports resolve.
_BACKEND = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)

from app import app  # noqa: E402

# Vercel's Python runtime looks for a WSGI callable named `app`.
app = app
