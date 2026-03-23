"""
WSGI entry point for production servers (Gunicorn, etc).
"""

from app.main import app

# For Gunicorn: gunicorn app.wsgi:app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
