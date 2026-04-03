from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app.services.analytics_service import AnalyticsService
from app.utils.response import ApiResponse

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route("/analytics")
@login_required
def dashboard():
    """Institutional SaaS Control Center v4.4"""
    # Note: Using the master dashboard as analytics hub
    metrics = AnalyticsService.get_dashboard_metrics()
    return render_template("analytics.html", metrics=metrics)

@analytics_bp.route("/api/analytics/stock")
@login_required
def api_stock_dist():
    """Real-time Phenotype Distribution JSON Feed."""
    dist = AnalyticsService.get_stock_distribution()
    return ApiResponse.success(dist)
