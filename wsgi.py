from app import create_app

# SaaS Production Interface (v4.0.0-PROD)
# Execution: gunicorn --bind 0.0.0.0:8000 wsgi:app

app = create_app()

if __name__ == "__main__":
    app.run()
