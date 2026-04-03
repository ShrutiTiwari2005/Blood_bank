from app.repositories.donor_repository import DonorRepository
from app.services.activity_service import ActivityService
from flask_login import current_user

class DonorService:
    """SaaS Donor Registry Logic v4.0"""

    @staticmethod
    def register_donor(name, age, blood_group, city, phone, last_donation):
        """Clinical Registration Protocol with Medical Validation."""
        try:
            # Business Rule: Minimum Age
            if int(age) < 18:
                return {"status": "error", "message": "Donor must be at least 18 years old."}
            
            # Create Record
            donor_id = DonorRepository.create(name, age, blood_group, city, phone, last_donation)
            
            # Audit Trail
            ActivityService.log_activity(
                user_id=current_user.id if current_user.is_authenticated else None,
                action="New Donor Registered",
                resource=name,
                affected_id=donor_id
            )
            
            return {"status": "success", "message": "Donor registered successfully."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def get_donors_nearby(city, blood_group):
        """Regional Phenotype Search Interface."""
        try:
            donors = DonorRepository.find_by_city_and_group(city, blood_group)
            return {"status": "success", "data": donors}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def get_all_donors():
        """National Master Donor Registry."""
        return DonorRepository.get_all()
