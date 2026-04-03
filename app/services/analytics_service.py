from app.repositories.stock_repo import StockRepository
from app.repositories.request_repo import RequestRepository
from app.repositories.donor_repo import DonorRepository
from app.repositories.patient_repo import PatientRepo

class AnalyticsService:
    """Institutional Analytics & Data Intelligence Hub v4.4"""

    @staticmethod
    def get_dashboard_metrics():
        """Aggregates national clinical metrics for the SaaS Control Center."""
        stock = StockRepository.get_all_stock()
        requests = RequestRepository.get_all_requests()
        donors = DonorRepository.get_all_donors()
        patients = PatientRepo.get_all_patients()

        # Calculation Metrics
        total_units = sum(s['units_available'] for s in stock)
        pending_requests = len([r for r in requests if r['status'] == 'pending'])
        critical_patients = len([p for p in patients if p['priority_level'] == 'critical'])
        
        # Regional Distribution
        regions = list(set([s['city'] for s in stock]))
        
        return {
            "total_units": total_units,
            "pending_requests": pending_requests,
            "critical_patients": critical_patients,
            "total_donors": len(donors),
            "region_count": len(regions),
            "stock_data": stock,
            "request_trends": requests[-10:] # Last 10 audit entries
        }

    @staticmethod
    def get_stock_distribution():
        """JSON Feed for Regional Stock Distribution Charting."""
        stock = StockRepository.get_all_stock()
        dist = {}
        for s in stock:
            dist[s['blood_group']] = dist.get(s['blood_group'], 0) + s['units_available']
        return dist
