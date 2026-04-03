from app.repositories.patient_repo import PatientRepo
from app.services.activity_service import ActivityService
from flask_login import current_user

class PatientService:
    """Medical Patient Intelligence & Priority Engine v4.4"""

    @staticmethod
    def get_priority_level(hb_level):
        """Clinical Priority Determination Node."""
        if hb_level < 8.0:
            return 'critical'
        elif 8.0 <= hb_level < 10.0:
            return 'high'
        return 'normal'

    @staticmethod
    def register_patient(data):
        """Standardized Institutional Registration Flow."""
        try:
            # 1. Automatic Priority Determination
            data['priority_level'] = PatientService.get_priority_level(float(data['current_hb']))
            
            # 2. Persist to Registry
            patient_id = PatientRepo.create_patient(data)
            
            # 3. Audit Trail
            ActivityService.log_activity(
                user_id=current_user.id if current_user.is_authenticated else None,
                action="Patient Onboarding Hub",
                resource=f"P-{patient_id}",
                metadata={"priority": data['priority_level'], "hb": data['current_hb']}
            )
            
            return {"status": "success", "message": f"Patient synchronized with {data['priority_level'].upper()} priority."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def get_all_patients():
        """National Health Registry Feed."""
        return PatientRepo.get_all_patients()

    @staticmethod
    def analyze_blood_report(hb, rbc):
        """Diagnostic Report Analyzer Logic (Guidance Only)."""
        metrics = {
            "hb_status": "Low" if hb < 11.0 else "Normal",
            "rbc_status": "Low" if rbc < 4.0 else "Normal",
            "clinical_guidance": "Immediate Blood Procurement required." if hb < 8.0 else "Monitor health metrics regularly."
        }
        return metrics
