from app.repositories.stock_repo import StockRepository
from app.repositories.request_repo import RequestRepository
from app.repositories.donor_repo import DonorRepository
from app.services.activity_service import ActivityService
from flask_login import current_user

class StockService:
    """Elite Inventory Logic Layer v4.0"""

    @staticmethod
    def get_inventory():
        """Fetches the global inventory of blood stock."""
        return StockRepository.get_all_stock()

    @staticmethod
    def handle_blood_request(city, blood_group, units):
        """Standardized Requisition Flow with Audit Logging."""
        # 1. Procurement Log entry
        req_id = RequestRepository.create_blood_request(
            city, blood_group, units, 
            user_id=current_user.id if current_user.is_authenticated else None
        )

        # 2. Audit Trail
        ActivityService.log_activity(
            user_id=current_user.id if current_user.is_authenticated else None,
            action="Blood Requisition Initiated",
            resource=f"{city} {blood_group}",
            affected_id=req_id
        )

        # 3. Decision Logic: Check stock
        stock = StockRepository.get_stock_by_city_and_group(city, blood_group)
        
        if stock and stock["units_available"] >= units:
            return {
                "status": "success",
                "message": "Stock validation successful. Procurement approved.",
                "data": {"action": "approve", "donors": None}
            }
        
        # 4. If insufficient, find donors
        donors = DonorRepository.find_by_city_and_group(city, blood_group)
        return {
            "status": "warning",
            "message": "Stock insufficient. AI donor-matching activated.",
            "data": {"action": "match", "donors": donors}
        }

    @staticmethod
    def procure_stock(city, blood_group, units):
        """Clinical Stock Refresh with Audit Trail."""
        try:
            StockRepository.update_stock_units(city, blood_group, units)
            ActivityService.log_activity(
                user_id=current_user.id if current_user.is_authenticated else None,
                action="Stock Procured",
                resource=f"{city} {blood_group}",
                metadata={"units": units}
            )
            return {"status": "success", "message": f"Successfully added {units} units."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def get_all_requests():
        """National Procurement Audit Trail."""
        return RequestRepository.get_all_requests()
