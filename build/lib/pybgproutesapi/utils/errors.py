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

def handle_error_response(response, content):
    detail = content.get("detail") if isinstance(content, dict) else None
    status = response.status_code

    if status == 403:
        raise InvalidAPIKeyError(f"Invalid API key: {detail}")
    elif status == 429:
        raise RateLimitError(f"Rate limit exceeded: {detail}")
    elif status == 400:
        raise BadRequestError(f"Invalid request: {detail}")
    elif status == 404:
        raise NotFoundError(f"Not found: {detail}")
    elif 500 <= status < 600:
        raise ServerError(f"Server error ({status}): {detail}")
    else:
        raise BGPAPIError(f"Unexpected error ({status}): {detail}")