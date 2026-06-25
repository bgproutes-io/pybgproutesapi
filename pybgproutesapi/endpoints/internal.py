from typing import Any, List, Optional, Tuple, Union

from ..utils.query import _csv, get, post
from ..utils.vp import VPBMP


def _prefix_filter_csv(prefix_filter: Optional[Union[List[Tuple[str, str]], str]]) -> Optional[str]:
    if isinstance(prefix_filter, list):
        return ",".join(f"{op}:{prefix}" for op, prefix in prefix_filter)
    return prefix_filter


def _bmp_vp_id(vp: Union[VPBMP, int]) -> int:
    if isinstance(vp, VPBMP):
        return int(vp.unique_id)
    return int(vp)


def bmp_rib_with_status(
    vp: Union[VPBMP, int],
    date: str,
    visibility: str = "all",
    data_afi: Optional[int] = None,
    prefix_filter: Optional[Union[List[Tuple[str, str]], str]] = None,
    prefix_exact_match: Optional[Union[List[str], str]] = None,
    aspath_regexp: Optional[str] = None,
    aspath_exact_match: Optional[Union[List[str], str]] = None,
    community_regexp: Optional[str] = None,
    return_aspath: bool = True,
    return_community: bool = True,
    return_rov_status: bool = True,
    rov_status_filter: Optional[Union[List[str], str]] = None,
    return_aspa_status: bool = True,
    aspa_status_filter: Optional[Union[List[str], str]] = None,
    start_index: Optional[int] = None,
    stop_index: Optional[int] = None,
    details: bool = False,
    base_url: str = None,
    api_key: str = None,
) -> Any:
    """Query `/bmp_rib_with_status` for one BMP VP."""
    params = {
        "vp_bmp_id": _bmp_vp_id(vp),
        "visibility": visibility,
        "date": date,
        "data_afi": data_afi,
        "prefix_filter": _prefix_filter_csv(prefix_filter),
        "prefix_exact_match": _csv(prefix_exact_match),
        "aspath_regexp": aspath_regexp,
        "aspath_exact_match": _csv(aspath_exact_match),
        "community_regexp": community_regexp,
        "return_aspath": return_aspath,
        "return_community": return_community,
        "return_rov_status": return_rov_status,
        "rov_status_filter": _csv(rov_status_filter),
        "return_aspa_status": return_aspa_status,
        "aspa_status_filter": _csv(aspa_status_filter),
        "start_index": start_index,
        "stop_index": stop_index,
    }

    if (
        isinstance(prefix_exact_match, list)
        and len(prefix_exact_match) > 10
    ) or (
        isinstance(aspath_exact_match, list)
        and len(aspath_exact_match) > 10
    ):
        return post("/bmp_rib_with_status", params, details, base_url=base_url, api_key=api_key)
    return get("/bmp_rib_with_status", params, details, base_url=base_url, api_key=api_key)


def bmp_updates_for_analysis(
    vp: Union[VPBMP, int],
    start_date: str,
    end_date: str,
    adj_rib_type: Optional[str] = None,
    visibility: str = "all",
    data_afi: Optional[int] = None,
    chronological_order: bool = True,
    max_updates_to_return: Optional[int] = None,
    prefix_filter: Optional[Union[List[Tuple[str, str]], str]] = None,
    prefix_exact_match: Optional[Union[List[str], str]] = None,
    aspath_regexp: Optional[str] = None,
    community_regexp: Optional[str] = None,
    return_aspath: bool = True,
    return_community: bool = True,
    return_rov_status: bool = True,
    rov_status_filter: Optional[Union[List[str], str]] = None,
    return_aspa_status: bool = True,
    aspa_status_filter: Optional[Union[List[str], str]] = None,
    details: bool = False,
    base_url: str = None,
    api_key: str = None,
) -> Any:
    """Query `/bmp_updates_for_analysis` for one BMP VP."""
    params = {
        "vp_bmp_id": _bmp_vp_id(vp),
        "adj_rib_type": adj_rib_type,
        "visibility": visibility,
        "start_date": start_date,
        "end_date": end_date,
        "data_afi": data_afi,
        "chronological_order": chronological_order,
        "max_updates_to_return": max_updates_to_return,
        "prefix_filter": _prefix_filter_csv(prefix_filter),
        "prefix_exact_match": _csv(prefix_exact_match),
        "aspath_regexp": aspath_regexp,
        "community_regexp": community_regexp,
        "return_aspath": return_aspath,
        "return_community": return_community,
        "return_rov_status": return_rov_status,
        "rov_status_filter": _csv(rov_status_filter),
        "return_aspa_status": return_aspa_status,
        "aspa_status_filter": _csv(aspa_status_filter),
    }

    if isinstance(prefix_exact_match, list) and len(prefix_exact_match) > 10:
        return post("/bmp_updates_for_analysis", params, details, base_url=base_url, api_key=api_key)
    return get("/bmp_updates_for_analysis", params, details, base_url=base_url, api_key=api_key)


def route_propagation_path(
    received_vp: Union[VPBMP, int],
    prefix: str,
    timestamp: float,
    aspath: str,
    communities: Optional[Union[List[str], str]] = None,
    nexthop: Optional[str] = None,
    local_pref: Optional[int] = None,
    med: Optional[int] = None,
    max_depth: int = 32,
    details: bool = False,
    base_url: str = None,
    api_key: str = None,
) -> Any:
    """Trace a route propagation path from one received BMP route."""
    params = {
        "received_vp_bmp_id": _bmp_vp_id(received_vp),
        "prefix": prefix,
        "timestamp": timestamp,
        "aspath": aspath,
        "communities": _csv(communities),
        "nexthop": nexthop,
        "local_pref": local_pref,
        "med": med,
        "max_depth": max_depth,
    }
    return get("/route_propagation_path", params, details, base_url=base_url, api_key=api_key)
