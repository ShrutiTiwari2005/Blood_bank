from flask import Flask, jsonify, request
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from .config import Config
import mysql.connector

# Initialize Elite Extensions
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    """Application Factory Pattern - SaaS Production Architecture v4.4"""
    app = Flask(__name__)
    
    app.config.from_object(Config)

    # Hardened SaaS Security
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800 # 30 mins
    
    # Initialize Extensions
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    csrf.init_app(app)

    # Register Blueprints (v4.4 Surgical Alignment)
    from app.routes.main_routes import main_bp
    from app.routes.donor_routes import donor_bp
    from app.routes.stock_routes import stock_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.api_routes import api_bp
    from app.routes.patient_routes import patient_bp
    from app.routes.analytics_routes import analytics_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(donor_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(analytics_bp)

    # Import User Loader from Service Logic
    from app.services.auth_service import load_user
    
    from app.utils.db import DatabaseManager

    # Global System Context
    @app.context_processor
    def inject_system_status():
        """Globally inject database connectivity and security status."""
        from flask_login import current_user
        return dict(
            db_status=DatabaseManager.is_connected(),
            app_version="v4.4.0-ARCHITECT",
            current_user=current_user
        )

    # Global Error Handlers (SaaS Standard)
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"status": "error", "message": "Requisition Timeout/Validation Failure.", "data": {}}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        if request.path.startswith('/api/'):
            return jsonify({"status": "error", "message": "Clinical Auth Required.", "data": {}}), 401
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))

    @app.errorhandler(404)
    def page_not_found(e):
        from flask import render_template
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"status": "error", "message": "Critical System Diagnostic Failure.", "data": {}}), 500

    @app.errorhandler(mysql.connector.Error)
    @app.errorhandler(mysql.connector.DatabaseError)
    def handle_db_error(e):
        from flask import render_template
        # SaaS Standard: Mask raw errors to prevent schema leakage
        return render_template("errors/db_error.html", error="Clinical Synchronization Node Offline. Check network connectivity."), 500

    return app
