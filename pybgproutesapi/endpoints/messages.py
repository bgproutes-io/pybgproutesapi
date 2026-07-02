from typing import Any, List, Optional, Tuple, Union

from ..utils.query import _csv, get
from ..utils.vp import VPBGP, VPBMP


def _prefix_filter_csv(prefix_filter: Optional[Union[List[Tuple[str, str]], str]]) -> Optional[str]:
    if isinstance(prefix_filter, list):
        return ",".join(f"{op}:{prefix}" for op, prefix in prefix_filter)
    return prefix_filter


def messages(
    vps: Union[VPBGP, VPBMP, List[Union[VPBGP, VPBMP]]],
    start_date: str,
    end_date: str,
    interval_time: int = 60,
    prefix_filter: Optional[Union[List[Tuple[str, str]], str]] = None,
    prefix_exact_match: Optional[Union[List[str], str]] = None,
    aspath_regexp: Optional[str] = None,
    aspath_exact_match: Optional[Union[List[str], str]] = None,
    community_regexp: Optional[str] = None,
    rov_status_filter: Optional[Union[List[str], str]] = None,
    aspa_status_filter: Optional[Union[List[str], str]] = None,
    bmp_visibility: Optional[str] = None,
    details: bool = False,
    base_url: str = None,
    api_key: str = None,
) -> Any:
    """Count BGP/BMP messages in fixed-size time buckets."""
    if isinstance(vps, (VPBGP, VPBMP)):
        vps = [vps]

    vp_bgp_ids = []
    vp_bmp_ids = []
    for vp in vps:
        if vp.peering_protocol == "bgp":
            vp_bgp_ids.append(vp.unique_id)
        else:
            vp_bmp_ids.append(vp.unique_id)

    params = {
        "vp_bgp_ids": _csv(vp_bgp_ids) if vp_bgp_ids else None,
        "vp_bmp_ids": _csv(vp_bmp_ids) if vp_bmp_ids else None,
        "start_date": start_date,
        "end_date": end_date,
        "interval_time": interval_time,
        "prefix_filter": _prefix_filter_csv(prefix_filter),
        "prefix_exact_match": _csv(prefix_exact_match),
        "aspath_regexp": aspath_regexp,
        "aspath_exact_match": _csv(aspath_exact_match),
        "community_regexp": community_regexp,
        "rov_status_filter": _csv(rov_status_filter),
        "aspa_status_filter": _csv(aspa_status_filter),
        "bmp_visibility": bmp_visibility,
    }
    return get("/messages", params, details, base_url=base_url, api_key=api_key)
