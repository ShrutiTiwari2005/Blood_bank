from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app.services.stock_service import StockService

stock_bp = Blueprint('stock', __name__)

@stock_bp.route("/blood_stock")
@login_required
def blood_stock():
    data = StockService.get_inventory()
    return render_template("blood_stock.html", data=data)

@stock_bp.route("/blood_request", methods=["GET","POST"])
@login_required
def blood_request():
    message = None
    donors = None
    if request.method == "POST":
        city = request.form["city"]
        blood_group = request.form["blood_group"]
        units = int(request.form["units"])
        
        result = StockService.handle_blood_request(city, blood_group, units)
        message = result["message"]
        donors = result["donors"]
        
    return render_template("blood_request.html", message=message, donors=donors)

@stock_bp.route("/requests")
@login_required
def requests():
    data = StockService.get_all_requests()
    return render_template("requests.html", data=data)
