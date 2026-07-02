from typing import Any, List, Optional, Union

from ..utils.query import _csv, get


def monitoring(
    start_date: str,
    end_date: str,
    bmp_parent_ips: Optional[Union[List[str], str]] = None,
    bmp_parent_asns: Optional[Union[List[int], str]] = None,
    frequency: Optional[int] = None,
    details: bool = False,
    base_url: str = None,
    api_key: str = None,
) -> Any:
    """Aggregate BMP update counters per BMP parent session."""
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "bmp_parent_ips": _csv(bmp_parent_ips),
        "bmp_parent_asns": _csv(bmp_parent_asns),
        "frequency": frequency,
    }
    return get("/monitoring", params, details, base_url=base_url, api_key=api_key)
