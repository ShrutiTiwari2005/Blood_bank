from app import create_app
from app.config import Config

# Create the application instance
application = create_app()

if __name__ == "__main__":
    # In production, use a WSGI server like Gunicorn or uWSGI
    application.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)
