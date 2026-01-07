from typing import List, Optional, Any, Dict, Union, Tuple
from ..utils.vp import VPBGP, VPBMP
from ..utils.query import get, post, _csv

def topology(
    vps: Union[VPBGP, VPBMP, List[Union[VPBGP, VPBMP]]],
    date: str,
    date_end: str = None,
    data_afi: int = None,
    bmp_feed_type: Optional[Union[List[str], str]] = None,
    directed: bool = False,
    with_aspath: bool = False,
    with_updates: bool = False,
    with_rib: bool = True,
    as_to_ignore: Optional[Union[List[int], str]] = None,
    ignore_private_asns: bool = False,
    details: bool = False,
    base_url: str = None,
    api_key: str = None,
) -> Any:
    """
    Fetch the AS-level topology built from the RIB/updates of multiple vantage points.

    :param vps: A VP object (VPBGP or VPBMP), or a list of VP objects.
    :param date: ISO format date string (YYYY-MM-DDTHH:MM:SS).
    :param date_end: End date (time interval), ISO format date string (YYYY-MM-DDTHH:MM:SS).
    :param directed: If true, the graph will be directed.
    :param with_aspath: If true, also return the AS paths used to build the topology.
    :param with_updates: If true, include AS paths observed in updates for the given day.
    :param with_rib: If true, include AS paths observed in RIBs for the given day.
    :param as_to_ignore: List of ASNs (or CSV string) to ignore.
    :param ignore_private_asns: If True, strip private ASNs from paths.
    :param details: If true, return the full API response including metadata.
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
        "bmp_feed_type": _csv(bmp_feed_type),
        "date": date,
        "date_end": date_end,
        "data_afi": data_afi,
        "directed": directed,
        "with_aspath": with_aspath,
        "with_updates": with_updates,
        "with_rib": with_rib,
        "as_to_ignore": ",".join(map(str, as_to_ignore)) if isinstance(as_to_ignore, list) else as_to_ignore,
        "ignore_private_asns": ignore_private_asns,
    }

    if len(vp_bgp_ids) + len(vp_bmp_ids) > 10 or (as_to_ignore is not None and len(as_to_ignore) > 10):
        return post("/topology", params, details, base_url=base_url, api_key=api_key)
    else:
        return get("/topology", params, details, base_url=base_url, api_key=api_key)
