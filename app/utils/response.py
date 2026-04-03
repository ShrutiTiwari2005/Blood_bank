from flask import jsonify

class ApiResponse:
    """Standardized API Response Governance v4.0"""
    
    @staticmethod
    def success(data=None, message="Success"):
        """200 OK - Standard SaaS Success"""
        return jsonify({
            "status": "success",
            "data": data or {},
            "message": message
        }), 200

    @staticmethod
    def error(message="Error", data=None, code=400):
        """Standardized Error Responses"""
        return jsonify({
            "status": "error",
            "data": data or {},
            "message": message
        }), code

    @staticmethod
    def unauthorized(message="Authentication Required"):
        """401 Unauthorized"""
        return ApiResponse.error(message, code=401)

    @staticmethod
    def forbidden(message="Insufficient Permissions"):
        """403 Forbidden"""
        return ApiResponse.error(message, code=403)

    @staticmethod
    def server_error(message="Internal Server Failure"):
        """500 Internal Server Error"""
        return ApiResponse.error(message, code=500)
