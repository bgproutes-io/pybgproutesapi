import os
import requests
from typing import List, Optional, Dict, Any, Union
from ._constants import BASE_URL
from ._errors import (
    BGPAPIError,
    InvalidAPIKeyError,
    RateLimitError,
    BadRequestError,
    NotFoundError,
    ServerError
)

def _handle_error_response(response, content):
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



def _get(path: str, params: Dict[str, Any], resource_details: bool = False) -> Any:
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
        _handle_error_response(response, content)

    if "data" not in content:
        raise BGPAPIError("Missing 'data' field in API response.")

    return content if resource_details else content["data"]


def _post(path: str, json_payload: Dict[str, Any], resource_details: bool = False) -> Any:
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
        _handle_error_response(response, content)

    if "data" not in content:
        raise BGPAPIError("Missing 'data' field in API response.")

    return content if resource_details else content["data"]
    

def vantage_points(
    vp_ips: Optional[List[str]] = None,
    vp_asns: Optional[List[int]] = None,
    ip_protocol: Optional[str] = None,
    source: Optional[List[str]] = None,
    country: Optional[List[str]] = None,
    rib_size_v4: Optional[tuple] = None,
    rib_size_v6: Optional[tuple] = None,
    return_uptime_intervals: bool = False,
    resource_details: bool = False
) -> Any:
    params = {
        "vp_ips": ",".join(vp_ips) if vp_ips else None,
        "vp_asns": ",".join(map(str, vp_asns)) if vp_asns else None,
        "ip_protocol": ip_protocol,
        "source": ",".join(source) if source else None,
        "country": ",".join(country) if country else None,
        "rib_size_v4": f"{rib_size_v4[0]},{rib_size_v4[1]}" if rib_size_v4 else None,
        "rib_size_v6": f"{rib_size_v6[0]},{rib_size_v6[1]}" if rib_size_v6 else None,
        "return_uptime_intervals": return_uptime_intervals
    }
    return _get("/vantage_points", params, resource_details)


def updates(
    vp_ip: Union[str, Dict[str, Any]],
    start_date: str,
    end_date: str,
    return_count: bool = False,
    chronological_order: bool = True,
    max_updates_to_return: Optional[int] = None,
    with_as_set: bool = True,
    type_filter: Optional[str] = None,
    prefix_filter: Optional[List[tuple]] = None,
    prefix_exact_match: Optional[List[str]] = None,
    return_aspath: bool = True,
    aspath_exact_match: Optional[List[str]] = None,
    aspath_regexp: Optional[str] = None,
    return_community: bool = True,
    community_regexp: Optional[str] = None,
    resource_details: bool = False,
    raise_error_bogus_vp: bool = False
) -> Any:
    if isinstance(vp_ip, dict) and 'ip' in vp_ip:
        vp_ip = vp_ip['ip']

    # ---- Type validation ----
    if prefix_exact_match is not None and not isinstance(prefix_exact_match, list):
        raise TypeError("prefix_exact_match must be a list of strings.")
    if aspath_exact_match is not None and not isinstance(aspath_exact_match, list):
        raise TypeError("aspath_exact_match must be a list of strings.")
    if prefix_filter is not None and (not isinstance(prefix_filter, list) or not all(isinstance(p, tuple) and len(p) == 2 for p in prefix_filter)):
        raise TypeError("prefix_filter must be a list of (operator, prefix) tuples.")
    # -------------------------

    pf_str = ",".join(f"{op}:{prefix}" for op, prefix in prefix_filter) if prefix_filter else None
    params = {
        "vp_ip": vp_ip,
        "start_date": start_date,
        "end_date": end_date,
        "return_count": return_count,
        "chronological_order": chronological_order,
        "max_updates_to_return": max_updates_to_return,
        "with_as_set": with_as_set,
        "type_filter": type_filter,
        "prefix_filter": pf_str,
        "prefix_exact_match": ",".join(prefix_exact_match) if prefix_exact_match else None,
        "return_aspath": return_aspath,
        "aspath_exact_match": ",".join(aspath_exact_match) if aspath_exact_match else None,
        "aspath_regexp": aspath_regexp,
        "return_community": return_community,
        "community_regexp": community_regexp,
        "raise_error_bogus_vp": raise_error_bogus_vp
    }
    if (aspath_exact_match is not None and len(aspath_exact_match) > 10) or (prefix_exact_match is not None and len(prefix_exact_match) > 10):
        return _post("/updates", params, resource_details)
    else:
        return _get("/updates", params, resource_details)


def rib(
    vp_ips: Union[List[str], List[Dict[str, Any]]],
    date: str,
    prefix_filter: Optional[List[tuple]] = None,
    prefix_exact_match: Optional[List[str]] = None,
    return_aspath: bool = True,
    aspath_exact_match: Optional[List[str]] = None,
    aspath_regexp: Optional[str] = None,
    return_community: bool = True,
    community_regexp: Optional[str] = None,
    return_count: bool = False,
    with_as_set: bool = True,
    resource_details: bool = False,
    raise_error_bogus_vp: bool = False,
) -> Any:
    # Extract IPs if input is list of dicts with 'ip' key
    if isinstance(vp_ips, list) and all(isinstance(d, dict) and 'ip' in d for d in vp_ips):
        vp_ips = [vp["ip"] for vp in vp_ips]

    # ---- Type validation ----
    if prefix_exact_match is not None and not isinstance(prefix_exact_match, list):
        raise TypeError("prefix_exact_match must be a list of strings.")
    if aspath_exact_match is not None and not isinstance(aspath_exact_match, list):
        raise TypeError("aspath_exact_match must be a list of strings.")
    if prefix_filter is not None and (not isinstance(prefix_filter, list) or not all(isinstance(p, tuple) and len(p) == 2 for p in prefix_filter)):
        raise TypeError("prefix_filter must be a list of (operator, prefix) tuples.")
    # -------------------------

    pf_str = ",".join(f"{op}:{prefix}" for op, prefix in prefix_filter) if prefix_filter else None

    params = {
        "vp_ips": ",".join(vp_ips),
        "date": date,
        "prefix_filter": pf_str,
        "prefix_exact_match": ",".join(prefix_exact_match) if prefix_exact_match else None,
        "return_aspath": return_aspath,
        "aspath_exact_match": ",".join(aspath_exact_match) if aspath_exact_match else None,
        "aspath_regexp": aspath_regexp,
        "return_community": return_community,
        "community_regexp": community_regexp,
        "return_count": return_count,
        "with_as_set": with_as_set,
        "raise_error_bogus_vp": raise_error_bogus_vp
    }

    if len(vp_ips) > 5 or (aspath_exact_match is not None and len(aspath_exact_match) > 10) or (prefix_exact_match is not None and len(prefix_exact_match) > 10):
        return _post("/rib", params, resource_details)
    else:
        return _get("/rib", params, resource_details)

def topology(
    vp_ips: Union[List[str], List[Dict[str, Any]]],
    date: str,
    directed: bool = False,
    with_aspath: bool = False,
    with_updates: bool = False,
    with_rib: bool = True,
    as_to_ignore: List[int] = [],
    resource_details: bool = False
) -> Any:
    """
    Fetch the AS-level topology built from the RIB of multiple vantage points.

    :param vp_ips: List of VP IPs or list of VP metadata dictionaries containing 'ip' key.
    :param date: ISO format date string (YYYY-MM-DDTHH:MM:SS).
    :param directed: If true, the graph will be directed.
    :param with_aspath: If true, also return the AS paths used to build the topology.
    :param with_updates: True possible only when the date is in format YYYY-DD-MM. If true, AS paths in updates observed within the given day are used to build the topology.
    :param with_rib: True possible only when the date is in format YYYY-DD-MM. If true, AS paths in a RIB observed within the given day are used to build the topology.
    :param as_to_ignore: List of ASes to ignore when building the topology and returing the AS path. Those typically include IXP ASN, private ASNs, etc.
    :param resource_details: If true, return the full API response including metadata.
    """
    # Extract plain IPs from dicts if needed
    if isinstance(vp_ips, list) and all(isinstance(d, dict) and 'ip' in d for d in vp_ips):
        vp_ips = [vp["ip"] for vp in vp_ips]

    params = {
        "vp_ips": ",".join(vp_ips),
        "date": date,
        "directed": directed,
        "with_aspath": with_aspath,
        "with_updates": with_updates,
        "with_rib": with_rib,
        "as_to_ignore": ",".join(map(str, as_to_ignore))
    }

    if len(vp_ips) > 5 or len(as_to_ignore) > 5:
        return _post("/topology", params, resource_details)
    else:
        return _get("/topology", params, resource_details)