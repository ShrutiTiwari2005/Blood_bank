from flask import Blueprint, render_template, request, redirect, url_for
from app.services.stock_service import StockService

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    """Elite v4.3 Landing Page (Master Hub)"""
    return render_template("index.html")

@main_bp.route("/dashboard")
def dashboard():
    """Clinical Operations Nerve Center (Requires Auth)"""
    from flask_login import login_required
    @login_required
    def protected_dashboard():
        data = StockService.get_inventory()
        return render_template("dashboard.html", data=data)
    return protected_dashboard()

@main_bp.route("/services")
def services():
    """SaaS Medical Services Suite"""
    return render_template("index.html", section="services")

@main_bp.route("/about")
def about():
    """Institutional Mission & GxP Standards"""
    return render_template("index.html", section="about")

@main_bp.route("/contact")
def contact():
    """Regional Hub Interface - Contact Center"""
    return render_template("index.html", section="contact")
