class AIGatewayException(Exception):
    """Base exception for all application-level errors"""
    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"
    
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class AuthenticationError(AIGatewayException):
    status_code = 401
    error_code = "AUTHENTICATION_ERROR"

class AuthorizationError(AIGatewayException):
    status_code = 403
    error_code = "AUTHORIZATION_ERROR"

class ValidationError(AIGatewayException):
    status_code = 400
    error_code = "VALIDATION_ERROR"

class ResourceNotFound(AIGatewayException):
    status_code = 404
    error_code = "RESOURCE_NOT_FOUND"

class DatabaseError(AIGatewayException):
    status_code = 500
    error_code = "DATABASE_ERROR"

class ConfigurationError(AIGatewayException):
    status_code = 500
    error_code = "CONFIGURATION_ERROR"

# Refactored for performance polish — 2026-06-07T12:14:23
