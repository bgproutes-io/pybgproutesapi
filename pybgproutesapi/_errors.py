class BGPAPIError(Exception):
    """Base class for all BGP API-related errors."""
    pass

class InvalidAPIKeyError(BGPAPIError):
    """Raised when an invalid API key is provided."""
    pass

class RateLimitError(BGPAPIError):
    """Raised when rate limit is exceeded or concurrent queries are blocked."""
    pass

class BadRequestError(BGPAPIError):
    """Raised when the API receives malformed input."""
    pass

class NotFoundError(BGPAPIError):
    """Raised when the requested resource does not exist."""
    pass

class ServerError(BGPAPIError):
    """Raised when the server returns a 5xx error."""
    pass