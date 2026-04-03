from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.patient_service import PatientService
from app.utils.response import ApiResponse

patient_bp = Blueprint('patient', __name__)

@patient_bp.route("/patients")
@login_required
def patients():
    """Institutional Patient Priority Dashboard v4.4"""
    data = PatientService.get_all_patients()
    return render_template("patients.html", patients=data)

@patient_bp.route("/onboard_patient", methods=["GET", "POST"])
@login_required
def onboard():
    """High-Risk Patient Registry Onboarding Node."""
    if request.method == "POST":
        data = {
            'name': request.form['name'],
            'age': request.form['age'],
            'blood_group': request.form['blood_group'],
            'current_hb': request.form['hb'],
            'condition_status': request.form['condition'],
            'city': request.form['city'],
            'phone': request.form['phone']
        }
        result = PatientService.register_patient(data)
        if result['status'] == 'success':
            flash(result['message'], 'success')
            return redirect(url_for('patient.patients'))
        flash(result['message'], 'error')
    
    return render_template("onboard_patient.html")

@patient_bp.route("/report_analyzer", methods=["GET", "POST"])
@login_required
def report_analyzer():
    """Medical Diagnostic Report Analyzer Node v4.4"""
    analysis = None
    if request.method == "POST":
        hb = float(request.form['hb'])
        rbc = float(request.form['rbc'])
        analysis = PatientService.analyze_blood_report(hb, rbc)
        analysis['hb'] = hb
        analysis['rbc'] = rbc
        
    return render_template("report_analyzer.html", analysis=analysis)

@patient_bp.route("/api/patient/analyze", methods=["POST"])
@login_required
def api_analyze():
    """JSON API Endpoint for Rapid Diagnostic Feed."""
    hb = request.json.get('hb')
    rbc = request.json.get('rbc')
    if hb is None or rbc is None:
        return ApiResponse.error("Missing medical blood parameters.")
    
    result = PatientService.analyze_blood_report(float(hb), float(rbc))
    return ApiResponse.success(result)
