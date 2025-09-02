from typing import List, Optional, Any, Dict, Union, Tuple
from ..utils.vp import VPBGP, VPBMP
from ..utils.query import get, post, _csv

def vantage_points(
    vp_bgp_ids: Optional[Union[List[str], str]] = None,
    vp_bmp_ids: Optional[Union[List[str], str]] = None,
    vp_ips: Optional[Union[List[str], str]] = None,
    vp_asns: Optional[Union[List[int], str]] = None,
    peering_protocol: Optional[Union[List[str], str]] = None,
    bmp_parent_ips: Optional[Union[List[str], str]] = None,
    bmp_parent_asns: Optional[Union[List[int], str]] = None,
    date: Optional[Union[str, List[str]]] = None,
    date_end: Optional[Union[str, List[str]]] = None,
    data_afi: Optional[Union[List[int], str]] = None,
    sources: Optional[Union[List[str], str]] = None,
    countries: Optional[Union[List[str], str]] = None,
    org_countries: Optional[Union[List[str], str]] = None,
    rib_size_v4: Optional[tuple] = None,
    rib_size_v6: Optional[tuple] = None,
    return_uptime_intervals: Optional[bool] = False,
    details: Optional[bool] = False,
) -> List[Union[VPBGP, VPBMP]]:
    # Normalize params to CSV where the API expects comma-separated strings
    params = {
        "vp_bgp_ids": _csv(vp_bgp_ids),
        "vp_bmp_ids": _csv(vp_bmp_ids),
        "vp_ips": _csv(vp_ips),
        "vp_asns": _csv(vp_asns),
        "peering_protocol": _csv(peering_protocol),
        "bmp_parent_ips": _csv(bmp_parent_ips),
        "bmp_parent_asns": _csv(bmp_parent_asns),
        "date": date,  # pass through (API may expect ISO string or day)
        "date_end": date_end,  # pass through (API may expect ISO string or day)
        "data_afi": _csv(data_afi),
        "sources": _csv(sources),
        "countries": _csv(countries),
        "org_countries": _csv(org_countries),
        "rib_size_v4": f"{rib_size_v4[0]},{rib_size_v4[1]}" if rib_size_v4 else None,
        "rib_size_v6": f"{rib_size_v6[0]},{rib_size_v6[1]}" if rib_size_v6 else None,
        "return_uptime_intervals": return_uptime_intervals
    }
    items = get("/vantage_points", params, details)

    if details:
        vp_items = items['data']
    else:
        vp_items = items

    vps: List[Union[VPBGP, VPBMP]] = []

    for it in vp_items.get('bgp', []):
        # Common fields with fallbacks for possible key names
        id = it.get("id")
        ip = it.get("ip")
        asn = it.get("asn")

        if id is None:
            continue

        # Optional common fields
        is_active = it.get('is_active')
        source_platform = it.get("source_platform")
        rib_size_v4 = it.get("rib_size_v4")
        rib_size_v6 = it.get("rib_size_v6")
        country = it.get("country")
        org_name = it.get("org_name")
        org_country = it.get("org_country")
        uptime_intervals = it.get("uptime_intervals")

        # Build objects
        vps.append(
            VPBGP(
                id=int(id),
                ip=str(ip),
                asn=int(asn),
                is_active=is_active,
                source_platform=source_platform,
                rib_size_v4=rib_size_v4,
                rib_size_v6=rib_size_v6,
                country=country,
                org_name=org_name,
                org_country=org_country,
                uptime_intervals=uptime_intervals,
            )
        )

    for it in vp_items.get('bmp', []):
        # Common fields with fallbacks for possible key names
        id = it.get("id")
        ip = it.get("ip")
        asn = it.get("asn")

        # Optional common fields
        is_active = it.get('is_active')
        source_platform = it.get("source_platform")
        rib_size_v4 = it.get("rib_size_v4")
        rib_size_v6 = it.get("rib_size_v6")
        country = it.get("country")
        org_name = it.get("org_name")
        org_country = it.get("org_country")
        uptime_intervals = it.get("uptime_intervals")

        # BMP-specific info can be nested or flat depending on your API
        peer_id = it.get("peer_id", {})
        bmp_info = it.get("bmp_info", {})
        bmp_parent_asn = bmp_info.get("parent_asn")
        bmp_parent_ip = bmp_info.get("parent_ip")
        bmp_feed_types = bmp_info.get("feed_types")

        vps.append(
            VPBMP(
                id=int(id),
                ip=str(ip),
                asn=int(asn),
                is_active=is_active,
                source_platform=source_platform,
                rib_size_v4=rib_size_v4,
                rib_size_v6=rib_size_v6,
                country=country,
                org_name=org_name,
                org_country=org_country,
                uptime_intervals=uptime_intervals,
                peer_id=peer_id,
                bmp_parent_asn=bmp_parent_asn,
                bmp_parent_ip=bmp_parent_ip,
                bmp_feed_types=[int(x) for x in bmp_feed_types] if bmp_feed_types else [],
            )
        )

    if details:
        return {'seconds': items['seconds'], 'bytes': items['bytes'], 'data': vps}
    else:
        return vps
