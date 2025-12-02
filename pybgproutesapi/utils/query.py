import os
import requests

from typing import List, Optional, Dict, Any, Union
from ..constants import BASE_URL
from .errors import (
    BGPAPIError,
    InvalidAPIKeyError,
    RateLimitError,
    BadRequestError,
    NotFoundError,
    ServerError,
    handle_error_response
)


def _csv(val: Optional[Union[List[Any], str]]) -> Optional[str]:
    """Accept list or comma-separated string and return CSV or None."""
    if val is None:
        return None
    if isinstance(val, str):
        return val
    return ",".join(map(str, val))


def get(path: str, params: Dict[str, Any], details: bool = True) -> Any:
    api_key = os.getenv("BGP_API_KEY")
    if not api_key:
        raise EnvironmentError("Missing environment variable: BGP_API_KEY")

    headers = {"x-api-key": api_key}
    clean_params = {k: v for k, v in params.items() if v is not None}

    response = requests.get(BASE_URL + path, headers=headers, params=clean_params, timeout=300)

    try:
        content = response.json()
    except Exception:
        raise requests.HTTPError(f"Invalid JSON response: {response.text}")

    if not response.ok:
        handle_error_response(response, content)

    if "data" not in content:
        raise BGPAPIError("Missing 'data' field in API response.")

    return content if details else content["data"]


def post(path: str, json_payload: Dict[str, Any], details: bool = True) -> Any:
    api_key = os.getenv("BGP_API_KEY")
    if not api_key:
        raise EnvironmentError("Missing environment variable: BGP_API_KEY")

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    response = requests.post(BASE_URL + path, headers=headers, json=json_payload, timeout=300)

    try:
        content = response.json()
    except Exception:
        raise requests.HTTPError(f"Invalid JSON response: {response.text}")

    if not response.ok:
        handle_error_response(response, content)

    if "data" not in content:
        raise BGPAPIError("Missing 'data' field in API response.")

    return content if details else content["data"]
    