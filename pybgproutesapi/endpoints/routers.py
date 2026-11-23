from typing import Any, Optional, Union, List

from .vantage_points import parse_vps
from ..utils.query import _csv, get


def parse_routers(items: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    parsed: dict[str, list[dict[str, Any]]] = {"bgp": [], "bmp": []}
    for protocol in ("bgp", "bmp"):
        for router in items.get(protocol, []) or []:
            router_item = dict(router)
            router_item["vantage_points"] = parse_vps(
                {protocol: router.get("vantage_points", []) or []}
            )
            parsed[protocol].append(router_item)
    return parsed


def routers(
    peering_protocol: Optional[str] = None,
    vp_asns: Optional[Union[List[int], str]] = None,
    bmp_parent_asns: Optional[Union[List[int], str]] = None,
    details: bool = False,
    base_url: str = None,
    api_key: str = None,
) -> Any:
    params = {
        "peering_protocol": peering_protocol,
        "vp_asns": _csv(vp_asns),
        "bmp_parent_asns": _csv(bmp_parent_asns),
    }
    response = get("/routers", params, details, base_url=base_url, api_key=api_key)
    if details:
        parsed = dict(response)
        parsed["data"] = parse_routers(response.get("data", {}))
        return parsed
    return parse_routers(response)
