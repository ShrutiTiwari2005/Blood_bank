from app.utils.db import DatabaseManager
import json

class ActivityService:
    """Medical Audit Trail & Activity Monitoring v4.0"""
    
    @staticmethod
    def log_activity(user_id, action, resource=None, affected_id=None, metadata=None):
        """Records a medical system action in the audit trail."""
        query = """
        INSERT INTO activity_logs (user_id, action, resource, affected_id, metadata)
        VALUES (%s, %s, %s, %s, %s)
        """
        metadata_json = json.dumps(metadata) if metadata else None
        
        try:
            return DatabaseManager.execute_modify(
                query, (user_id, action, resource, affected_id, metadata_json)
            )
        except Exception as e:
            # SaaS Principle: Fail-Safe Logging (Log to stdout if DB fails)
            print(f"AUDIT LOG FAILURE: {e} | Action: {action} | User: {user_id}")
            return None

    @staticmethod
    def get_recent_activity(limit=10):
        """Fetches the latest clinical audit logs."""
        query = """
            SELECT logs.*, users.username 
            FROM activity_logs logs
            LEFT JOIN users ON logs.user_id = users.id
            ORDER BY logs.timestamp DESC
            LIMIT %s
        """
        return DatabaseManager.execute_query(query, (limit,))
