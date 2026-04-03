from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.services.stock_service import StockService
from app.services.prediction_service import PredictionService
from app.services.donor_service import DonorService
from app.utils.response import ApiResponse

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route("/inventory")
@login_required
def get_inventory():
    """Real-time Inventory JSON Feed for Chart.js."""
    try:
        data = StockService.get_inventory()
        return ApiResponse.success(data)
    except Exception as e:
        return ApiResponse.server_error(str(e))

@api_bp.route("/requests")
@login_required
def get_requests():
    """National Procurement Audit Trail JSON Feed."""
    try:
        data = StockService.get_all_requests()
        return ApiResponse.success(data)
    except Exception as e:
        return ApiResponse.server_error(str(e))

@api_bp.route("/predict/shortage", methods=["POST"])
@login_required
def predict_shortage():
    """Diagnostic AI Shortage Endpoint."""
    city = request.json.get("city")
    blood_group = request.json.get("blood_group")
    units = request.json.get("units")
    
    if not all([city, blood_group, units]):
        return ApiResponse.error("Missing required phenotype data.")
        
    result = PredictionService.get_shortage_prediction(city, blood_group, units)
    # If the service already returns a status dict, we extract the data
    data = result.get("data") if isinstance(result, dict) and "data" in result else result
    return ApiResponse.success(data, message=result.get("message", "Success") if isinstance(result, dict) else "Success")

@api_bp.route("/model/status")
@login_required
def model_status():
    """AI Model Health & Version Registry Check."""
    result = PredictionService.get_model_health()
    return ApiResponse.success(result)

@api_bp.route("/donors/search", methods=["POST"])
@login_required
def search_donors():
    """Regional Phenotype Search Endpoint."""
    city = request.json.get("city")
    blood_group = request.json.get("blood_group")
    
    result = DonorService.get_donors_nearby(city, blood_group)
    return ApiResponse.success(result)
