from typing import List, Optional, Any, Dict, Union, Tuple
from .utils.vp import VPBGP, VPBMP
from .utils.query import get, post

def _csv(val: Optional[Union[List[Any], str]]) -> Optional[str]:
    """Accept list or comma-separated string and return CSV or None."""
    if val is None:
        return None
    if isinstance(val, str):
        return val
    return ",".join(map(str, val))

def vantage_points(
    vp_ids_bgp: Optional[Union[List[str], str]] = None,
    vp_ids_bmp: Optional[Union[List[str], str]] = None,
    vp_ips: Optional[Union[List[str], str]] = None,
    vp_asns: Optional[Union[List[int], str]] = None,
    peering_protocol: Optional[Union[List[str], str]] = None,
    date: Optional[Union[str, List[str]]] = None,
    data_afi: Optional[Union[List[int], str]] = None,
    source: Optional[Union[List[str], str]] = None,
    org_countries: Optional[Union[List[str], str]] = None,
    rib_size_v4: Optional[tuple] = None,
    rib_size_v6: Optional[tuple] = None,
    return_uptime_intervals: bool = False,
    resource_details: bool = False
) -> List[Union[VPBGP, VPBMP]]:
    # Normalize params to CSV where the API expects comma-separated strings
    params = {
        "vp_ids_bgp": _csv(vp_ids_bgp),
        "vp_ids_bmp": _csv(vp_ids_bmp),
        "vp_ips": _csv(vp_ips),
        "vp_asns": _csv(vp_asns),
        "peering_protocol": _csv(peering_protocol),
        "date": date,  # pass through (API may expect ISO string or day)
        "data_afi": _csv(data_afi),
        "source": _csv(source),
        "org_countries": _csv(org_countries),
        "rib_size_v4": f"{rib_size_v4[0]},{rib_size_v4[1]}" if rib_size_v4 else None,
        "rib_size_v6": f"{rib_size_v6[0]},{rib_size_v6[1]}" if rib_size_v6 else None,
        "return_uptime_intervals": return_uptime_intervals
    }
    items = get("/vantage_points", params, resource_details)
    vps: List[Union[VPBGP, VPBMP]] = []

    for it in items.get('bgp', []):
        # Common fields with fallbacks for possible key names
        id = it.get("id")
        ip = it.get("ip")
        asn = it.get("asn")

        # Optional common fields
        is_active = it.get('is_active')
        peer_country = it.get("peer_country")
        org_name = it.get("org_name")
        org_country = it.get("org_country")
        rib_size_v4 = it.get("rib_size_v4")
        rib_size_v6 = it.get("rib_size_v6")
        source_platform = it.get("source_platform")
        uptime_intervals = it.get("uptime_intervals")

        # Build objects
        vps.append(
            VPBGP(
                id=int(id),
                ip=str(ip),
                asn=int(asn),
                org_name=org_name,
                org_country=org_country,
                rib_size_v4=rib_size_v4,
                rib_size_v6=rib_size_v6,
                source_platform=source_platform,
                uptime_intervals=uptime_intervals,
            )
        )

    for it in items.get('bmp', []):
        # Common fields with fallbacks for possible key names
        id = it.get("unique_id")
        ip = it.get("ip")
        asn = it.get("asn")

        # Optional common fields
        peer_country = it.get("peer_country")
        org_name = it.get("org_name")
        org_country = it.get("org_country")
        rib_size_v4 = it.get("rib_size_v4")
        rib_size_v6 = it.get("rib_size_v6")
        source_platform = it.get("source_platform")
        uptime_intervals = it.get("uptime_intervals")

        # BMP-specific info can be nested or flat depending on your API
        bmp_info = it.get("bmp_info", {})
        bmp_parent_asn = bmp_info.get("parent_asn")
        bmp_parent_ip = bmp_info.get("parent_ip")
        bmp_feed_types = bmp_info.get("feed_types")

        vps.append(
            VPBMP(
                id=int(id),
                ip=str(ip),
                asn=int(asn),
                peer_country=peer_country,
                org_name=org_name,
                org_country=org_country_val,
                rib_size_v4=rib4,
                rib_size_v6=rib6,
                source_platform=source_platform,
                bmp_parent_asn=int(bmp_parent_asn) if bmp_parent_asn is not None else None,
                bmp_parent_ip=bmp_parent_ip,
                bmp_feed_types=[int(x) for x in bmp_feed_types] if bmp_feed_types else [],
                uptime_intervals=uptime,
            )
        )

    return vps


def updates(
    vp: Union[VPBGP, VPBMP],
    start_date: str,
    end_date: str,
    bmp_feed_types: Optional[Union[List[str], str]] = None,
    return_count: bool = False,
    chronological_order: bool = True,
    max_updates_to_return: Optional[int] = None,
    type_filter: Optional[str] = None,
    prefix_filter: Optional[Union[List[Tuple[str, str]], str]] = None,
    prefix_exact_match: Optional[Union[List[str], str]] = None,
    return_aspath: bool = True,
    aspath_exact_match: Optional[Union[List[str], str]] = None,
    aspath_regexp: Optional[str] = None,
    return_community: bool = True,
    community_regexp: Optional[str] = None,
    resource_details: bool = False,
    raise_error_bogus_vp: bool = False
) -> Any:

    # Normalize prefix_filter
    if isinstance(prefix_filter, list):
        pf_str = ",".join(f"{op}:{prefix}" for op, prefix in prefix_filter)
    else:
        pf_str = prefix_filter  # already a string or None

    params = {
        "vp_id": vp.id,
        "vp_peering_protocol": vp.peering_protocol,
        "bmp_feed_types": _csv(bmp_feed_types),
        "start_date": start_date,
        "end_date": end_date,
        "return_count": return_count,
        "chronological_order": chronological_order,
        "max_updates_to_return": max_updates_to_return,
        "type_filter": type_filter,
        "prefix_filter": pf_str,
        "prefix_exact_match": _csv(prefix_exact_match),
        "return_aspath": return_aspath,
        "aspath_exact_match": _csv(aspath_exact_match),
        "aspath_regexp": aspath_regexp,
        "return_community": return_community,
        "community_regexp": community_regexp,
        "raise_error_bogus_vp": raise_error_bogus_vp
    }

    # Use POST if too many exact matches, otherwise GET
    if (
        (isinstance(aspath_exact_match, list) and len(aspath_exact_match) > 10)
        or (isinstance(prefix_exact_match, list) and len(prefix_exact_match) > 10)
    ):
        return post("/updates", params, resource_details)
    else:
        return get("/updates", params, resource_details)

# vps = vantage_points(vp_ids_bgp=[1,2,3])
# for vp in vps:
#     print (vp)
#     l = updates(vp, start_date='2024-06-01T00:00:00', end_date='2024-06-02T00:00:00', prefix_exact_match=['17.0.0.0/8', '21.0.0.0/8', '22.0.0.0/8', '26.0.0.0/8', '28.0.0.0/8', '29.0.0.0/8', '30.0.0.0/8', '33.0.0.0/8', '38.0.0.0/8', '53.0.0.0/8', '55.0.0.0/8'])
#     print (l)

def rib(
    vps: Union[VPBGP | VPBMP, List[VPBGP | VPBMP]],
    date: str,
    bmp_feed_types: Optional[Union[List[str], str]] = None,
    prefix_filter: Optional[Union[List[Tuple[str, str]], str]] = None,
    prefix_exact_match: Optional[Union[List[str], str]] = None,
    return_aspath: bool = True,
    aspath_exact_match: Optional[Union[List[str], str]] = None,
    aspath_regexp: Optional[str] = None,
    return_community: bool = True,
    community_regexp: Optional[str] = None,
    return_count: bool = False,
    with_as_set: bool = True,
    resource_details: bool = False,
    raise_error_bogus_vp: bool = False,
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

    for vp in vps:
        if vp.peering_protocol == 'bgp':
            vp_bgp_ids.append(vp.id)
        else:
            vp_bmp_ids.append(vp.id)

    params = {
        "vp_bgp_ids": _csv(vp_bgp_ids) if vp_bgp_ids else None,
        "vp_bmp_ids": _csv(vp_bmp_ids) if vp_bmp_ids else None,
        "bmp_feed_types": _csv(bmp_feed_types),
        "date": date,
        "prefix_filter": pf_str,
        "prefix_exact_match": _csv(prefix_exact_match),
        "return_aspath": return_aspath,
        "aspath_exact_match": _csv(aspath_exact_match),
        "aspath_regexp": aspath_regexp,
        "return_community": return_community,
        "community_regexp": community_regexp,
        "return_count": return_count,
        "with_as_set": with_as_set,
        "raise_error_bogus_vp": raise_error_bogus_vp
    }

    # Use POST if large lists are provided
    if (len(vp_bgp_ids) + len(vp_bmp_ids) > 100
        or (isinstance(aspath_exact_match, list) and len(aspath_exact_match) > 10)
        or (isinstance(prefix_exact_match, list) and len(prefix_exact_match) > 10)
    ):
        return post("/rib", params, resource_details)
    else:
        return get("/rib", params, resource_details)

# vps = vantage_points(vp_ids_bgp=[1,2,3])
# r = rib(vps, date='2024-06-02T12:30:00', prefix_exact_match=['17.0.0.0/8', '21.0.0.0/8', '22.0.0.0/8', '26.0.0.0/8', '28.0.0.0/8', '29.0.0.0/8', '30.0.0.0/8', '33.0.0.0/8', '38.0.0.0/8', '53.0.0.0/8', '55.0.0.0/8'])
# for vp_id, rtmp in r['bgp'].items():
#     if rtmp != 'down':
#         for prefix, (aspath, comm) in list(rtmp.items())[:20]:
#             print (prefix, aspath, comm)



def topology(
    vps: Union[VPBGP, VPBMP, List[Union[VPBGP, VPBMP]]],
    date: str,
    bmp_feed_types: Optional[Union[List[str], str]] = None,
    directed: bool = False,
    with_aspath: bool = False,
    with_updates: bool = False,
    with_rib: bool = True,
    as_to_ignore: Optional[Union[List[int], str]] = None,
    ignore_private_asns: bool = False,
    resource_details: bool = False,
) -> Any:
    """
    Fetch the AS-level topology built from the RIB/updates of multiple vantage points.

    :param vps: A VP object (VPBGP or VPBMP), or a list of VP objects.
    :param date: ISO format date string (YYYY-MM-DDTHH:MM:SS).
    :param directed: If true, the graph will be directed.
    :param with_aspath: If true, also return the AS paths used to build the topology.
    :param with_updates: If true, include AS paths observed in updates for the given day.
    :param with_rib: If true, include AS paths observed in RIBs for the given day.
    :param as_to_ignore: List of ASNs (or CSV string) to ignore.
    :param ignore_private_asns: If True, strip private ASNs from paths.
    :param resource_details: If true, return the full API response including metadata.
    """

    # Normalize vps into a list of IPs
    if isinstance(vps, (VPBGP, VPBMP)):
        vps = [vps]

    vp_bgp_ids = []
    vp_bmp_ids = []

    for vp in vps:
        if vp.peering_protocol == 'bgp':
            vp_bgp_ids.append(vp.id)
        else:
            vp_bmp_ids.append(vp.id)

    params = {
        "vp_bgp_ids": _csv(vp_bgp_ids) if vp_bgp_ids else None,
        "vp_bmp_ids": _csv(vp_bmp_ids) if vp_bmp_ids else None,
        "bmp_feed_types": _csv(bmp_feed_types),
        "date": date,
        "directed": directed,
        "with_aspath": with_aspath,
        "with_updates": with_updates,
        "with_rib": with_rib,
        "as_to_ignore": ",".join(map(str, as_to_ignore)) if isinstance(as_to_ignore, list) else as_to_ignore,
        "ignore_private_asns": ignore_private_asns,
    }

    if len(vp_bgp_ids) + len(vp_bmp_ids) > 10 or (as_to_ignore is not None and len(as_to_ignore) > 10):
        return post("/topology", params, resource_details)
    else:
        return get("/topology", params, resource_details)

# vps = vantage_points(vp_ids_bgp=[1,2,3,4,5,6,7,8,9,10,11])
# t = topology(vps, date='2024-06-01', as_to_ignore=[29222])
# print (t)