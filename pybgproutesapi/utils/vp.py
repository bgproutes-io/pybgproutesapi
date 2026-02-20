from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Any, Dict

@dataclass
class VP:
    unique_id: int
    ip: str
    asn: int
    source: Optional[str] = None
    rib_size_v4: Optional[int] = None
    rib_size_v6: Optional[int] = None
    country: Optional[str] = None
    org_name: Optional[str] = None
    org_country: Optional[str] = None
    peering_protocol: Optional[str] = None
    status: Optional[Any] = None
    status_since: Optional[Any] = None
    status_history: Optional[Any] = None
    uptime_intervals: Optional[Any] = None

    def __eq__(self, other):
        if not isinstance(other, VP):
            return False
        return (
            self.peering_protocol == other.peering_protocol
            and self._get_comparison_key() == other._get_comparison_key()
        )

    def __hash__(self):
        return hash((self.peering_protocol, self._get_comparison_key()))

    def _get_comparison_key(self):
        raise NotImplementedError

    # ---------- Pretty printing ----------
    def __str__(self) -> str:
        proto = self.peering_protocol or "vp"
        country = f"[{self.country}]" if self.country else ""
        org = f"{self.org_name}" if self.org_name else ""
        src = f" | source: {self.source}" if self.source else ""
        parts = [str(self.unique_id), ':', proto, "-", f"{self.ip}", f"AS{self.asn}"]
        if country:
            parts.append(country)
        if org:
            parts.append(org)
        return " ".join(parts) + src

    def __repr__(self) -> str:
        return self.__str__()


@dataclass(eq=False)
class VPBGP(VP):
    status: str = None
    status_since: str = None
    status_history: List[Any] = None
    uptime_intervals: List[Any] = None

    def __post_init__(self):
        self.peering_protocol = "bgp"

    def _get_comparison_key(self):
        return (self.ip,)


@dataclass(eq=False)
class VPBMP(VP):
    peer_id: Optional[int] = None
    bmp_parent_org_name: str = None
    bmp_parent_asn: int = None
    bmp_parent_asn_country: int = None
    bmp_parent_ip: str = None
    bmp_parent_ip_country: str = None
    bmp_feed_types: List[int] = None
    status: Dict[str] = None
    status_since: Dict[str] = None
    status_history: Dict[Any] = None
    uptime_intervals: Dict[Any] = None

    # This is just an informational variable used within the code for optimizations but not given to the user.
    bmp_feed_types_all: List[int] = None

    def __post_init__(self):
        self.peering_protocol = "bmp"

    def _get_comparison_key(self):
        return (self.ip, self.asn, self.bmp_parent_ip, self.bmp_parent_asn, tuple(sorted(self.bmp_feed_types or [])))

    # ---------- Pretty printing with feed types ----------
    def __str__(self) -> str:
        feeds = ""
        if self.bmp_feed_types:
            feeds = f" ({', '.join(map(str, sorted(set(self.bmp_feed_types))))})"
        proto = f"bmp{feeds}"
        country = f"[{self.country}]" if self.country else ""
        org = f"{self.org_name}" if self.org_name else ""
        src = f" | source: {self.source}" if self.source else ""
        parts = [str(self.unique_id), ':', proto, "-", f"{self.ip}", f"AS{self.asn}"]
        if country:
            parts.append(country)
        if org:
            parts.append(org)
        return " ".join(parts) + src

    def __repr__(self) -> str:
        return self.__str__()
