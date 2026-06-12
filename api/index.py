"""Vercel serverless entrypoint.

Vercel's @vercel/python runtime detects the module-level ASGI ``app`` and
serves it. All routing is delegated to vercel.json, which rewrites every
request to this file.
"""

from app.main import app

__all__ = ["app"]
