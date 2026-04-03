from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.services.auth_service import AuthService
from app.utils.response import ApiResponse

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """SaaS Standardized Login Interface."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        result = AuthService.login_user(username, password)
        if result["status"] == "success":
            login_user(result["user"])
            return redirect(url_for('main.onboarding'))
        else:
            flash(result["message"], "error")
    
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Elite Registration Protocol Initialization."""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "viewer")
        
        result = AuthService.register_user(username, email, password, role)
        if result["status"] == "success":
            flash("Registration Successful. Please Login.", "success")
            return redirect(url_for('auth.login'))
        else:
            flash(result["message"], "error")
            
    return render_template("register.html") # We'll need to create this simple one or reuse onboarding

@auth_bp.route("/logout")
@login_required
def logout():
    """Session Termination Protocol."""
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route("/profile")
@login_required
def profile():
    """Institutional User Profile Interface."""
    return render_template("profile.html")

@auth_bp.route("/api/auth/status")
def auth_status():
    """JSON Auth Status for Frontend Sync."""
    if current_user.is_authenticated:
        return ApiResponse.success({
            "id": current_user.id,
            "username": current_user.username,
            "role": current_user.role
        })
    return ApiResponse.unauthorized()
