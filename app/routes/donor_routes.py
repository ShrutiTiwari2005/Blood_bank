from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app.services.donor_service import DonorService
from app.services.prediction_service import PredictionService

donor_bp = Blueprint('donor', __name__)

@donor_bp.route("/donar_predict", methods=["GET", "POST"])
@login_required
def donar():
    prediction = None
    if request.method == "POST":
        recency = request.form["recency"]
        frequency = request.form["frequency"]
        monetary = request.form["monetary"]
        time = request.form["time"]
        prediction = PredictionService.get_donor_prediction(recency, frequency, monetary, time)
    return render_template("donar_predict.html", prediction=prediction)

@donor_bp.route("/register_donor", methods=["GET","POST"])
@login_required
def register_donor():
    message = None
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        blood_group = request.form["blood_group"]
        city = request.form["city"]
        phone = request.form["phone"]
        last_donation = request.form["last_donation"]
        
        success, message = DonorService.register_donor(name, age, blood_group, city, phone, last_donation)
    return render_template("register_donor.html", message=message)

@donor_bp.route("/find_donor", methods=["GET","POST"])
@login_required
def find_donor():
    donors = None
    message = None
    if request.method == "POST":
        city = request.form["city"]
        blood_group = request.form["blood_group"]
        donors = DonorService.find_donors(city, blood_group)
        if not donors:
            message = "No matching donors available."
    return render_template("find_donor.html", donors=donors, message=message)

@donor_bp.route("/donor_list")
@login_required
def donor_list():
    donors = DonorService.get_all_donors()
    return render_template("donor_list.html", donors=donors)
