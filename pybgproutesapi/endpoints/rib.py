from typing import List, Optional, Any, Dict, Union, Tuple
from ..utils.vp import VPBGP, VPBMP
from ..utils.query import get, post, _csv

def rib(
    vps: Union[VPBGP | VPBMP, List[VPBGP | VPBMP]],
    date: str,
    bmp_feed_type: Optional[Union[List[str], str]] = None,
    data_afi: int = None,
    prefix_filter: Optional[Union[List[Tuple[str, str]], str]] = None,
    prefix_exact_match: Optional[Union[List[str], str]] = None,
    return_aspath: bool = True,
    aspath_exact_match: Optional[Union[List[str], str]] = None,
    aspath_regexp: Optional[str] = None,
    return_community: bool = True,
    community_regexp: Optional[str] = None,
    return_count: bool = False,
    with_as_set: bool = True,
    details: bool = False,
    base_url: str = None,
    return_rov_status: bool = False,
    return_aspa_status: bool = False,
    rov_status_filter: list[int] = None,
    aspa_status_filter: list[int] = None,
    api_key: str = None,
    version: str = "v1",
) -> Any:
    # Normalize prefix_filter
    if isinstance(prefix_filter, list):
        pf_str = ",".join(f"{op}:{prefix}" for op, prefix in prefix_filter)
    else:
        pf_str = prefix_filter  # already a string or None

    if not isinstance(vps, list):
        vps = [vps]

    vp_bgp_ids = []
    vp_bmp_ids = []

    if rov_status_filter is not None:
        rov_status_filter = ",".join([str(e) for e in rov_status_filter])

    if aspa_status_filter is not None:
        aspa_status_filter = ",".join([str(e) for e in aspa_status_filter])

    for vp in vps:
        if vp.peering_protocol == 'bgp':
            vp_bgp_ids.append(vp.id)
        else:
            vp_bmp_ids.append(vp.id)

    params = {
        "vp_bgp_ids": _csv(vp_bgp_ids) if vp_bgp_ids else None,
        "vp_bmp_ids": _csv(vp_bmp_ids) if vp_bmp_ids else None,
        "bmp_feed_type": _csv(bmp_feed_type),
        "date": date,
        "data_afi": data_afi,
        "prefix_filter": pf_str,
        "prefix_exact_match": _csv(prefix_exact_match),
        "return_aspath": return_aspath,
        "aspath_exact_match": _csv(aspath_exact_match),
        "aspath_regexp": aspath_regexp,
        "return_community": return_community,
        "community_regexp": community_regexp,
        "return_count": return_count,
        "with_as_set": with_as_set,
        "return_rov_status": return_rov_status,
        "return_aspa_status": return_aspa_status,
        "rov_status_filter": rov_status_filter,
        "aspa_status_filter": aspa_status_filter
    }

    # Use POST if large lists are provided
    if (len(vp_bgp_ids) + len(vp_bmp_ids) > 100
        or (isinstance(aspath_exact_match, list) and len(aspath_exact_match) > 10)
        or (isinstance(prefix_exact_match, list) and len(prefix_exact_match) > 10)
    ):
        return post(f"/{version}/rib", params, details, base_url=base_url, api_key=api_key)
    else:
        return get(f"/{version}/rib", params, details, base_url=base_url, api_key=api_key)

