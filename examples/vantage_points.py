from __future__ import annotations

import sys
from datetime import datetime, timedelta

from pybgproutesapi import vantage_points

# ---- Python-version-safe UTC handling ----
if sys.version_info >= (3, 11):
    from datetime import UTC as _UTC
else:
    from datetime import timezone as _timezone
    _UTC = _timezone.utc

SOURCES = ["ris", "bgproutes.io", "routeviews", "pch", "cgtf"]

# ---- Compute yesterday's date at 10:30:00 UTC ----
rib_date = (datetime.now(_UTC) - timedelta(days=1)).replace(
    hour=10, minute=30, second=0, microsecond=0
)
rib_date_str = rib_date.strftime("%Y-%m-%dT%H:%M:%S")

# ---- 24h interval end (variable name requested: date_end) ----
date_end = rib_date + timedelta(hours=24)
date_end_str = date_end.strftime("%Y-%m-%dT%H:%M:%S")


def run_vp_query(description: str, *, show_n: int = 10, **kwargs) -> None:
    print(f"\n- {description}")
    results = vantage_points(**kwargs)
    vps = results.get("data", []) or []

    print(f"  -> {len(vps)} VPs in {results.get('seconds')}s")
    print(f"  sample (up to {min(show_n, len(vps))}):")

    for i, vp in enumerate(vps[:show_n], start=1):
        # ----------------
        # Status + since
        # ----------------
        if vp.peering_protocol == "bgp":
            since = (
                vp.status_since.isoformat()
                if hasattr(vp.status_since, "isoformat")
                else vp.status_since
            )

            print(
                f"    {i:02d}. id={vp.id} protocol=bgp "
                f"status={vp.status} since={since}"
            )

        else:  # BMP
            ft_str = ",".join(map(str, vp.bmp_feed_types))
            print(
                f"    {i:02d}. id={vp.id} protocol=bmp "
                f"feed_types={ft_str}"
            )

            for ft, status in vp.status.items():
                raw_since = vp.status_since.get(ft)
                since = (
                    raw_since.isoformat()
                    if hasattr(raw_since, "isoformat")
                    else raw_since
                )
                print(f"        ft={ft} status={status} since={since}")


        # ----------------
        # Status history
        # ----------------
        # BGP history
        if vp.peering_protocol == "bgp":
            for ts, state, reason in list(reversed(vp.status_history))[:10]:
                ts_str = ts.isoformat() if hasattr(ts, "isoformat") else str(ts)
                print(f"          {ts_str} state={state} reason={reason}")

        # BMP history
        else:
            for ft, history in vp.status_history.items():
                print(f"          ft={ft}:")
                for ts, state, reason in list(reversed(history))[:10]:
                    ts_str = ts.isoformat() if hasattr(ts, "isoformat") else str(ts)
                    print(f"            {ts_str} state={state} reason={reason}")


for proto in ["bgp", "bmp"]:
    print(
        f"\n====================\n"
        f"Protocol: {proto.upper()}\n"
        f"date={rib_date_str}Z\n"
        f"date_end={date_end_str}Z\n"
        f"===================="
    )

    base_kwargs = dict(
        sources=SOURCES,
        peering_protocol=proto,
        details=True,
        return_status_history=True
    )

    # 1) No date filter (current snapshot / default behavior)
    run_vp_query(
        "List all VPs (no date filter), with details=True and return_status=False.",
        **base_kwargs,
    )


    # 1) No date filter (current snapshot / default behavior)
    run_vp_query(
        "List all VPs (no date filter), with details=True and return_status=False.",
        **base_kwargs,
        status=['up'],
    )

    # 1) No date filter (current snapshot / default behavior)
    run_vp_query(
        "List all VPs (no date filter), with details=True and return_status=False.",
        **base_kwargs,
        status=['down'],
    )

    # 2) With date filter
    run_vp_query(
        f"List all VPs at date={rib_date_str} (yesterday 10:30 UTC), with details=True and return_status=False.",
        **base_kwargs,
        date=rib_date_str,
    )

    # 3) With date + status=['ready']
    run_vp_query(
        f"List VPs at date={rib_date_str} filtered by status=['ready'].",
        **base_kwargs,
        date=rib_date_str,
        status=["ready"],
    )

    # 4) With date + status=['up']
    run_vp_query(
        f"List VPs at date={rib_date_str} filtered by status=['up'].",
        **base_kwargs,
        date=rib_date_str,
        status=["up"],
    )

    # 5) With date + status=['down']
    run_vp_query(
        f"List VPs at date={rib_date_str} filtered by status=['down'].",
        **base_kwargs,
        date=rib_date_str,
        status=["down"],
    )

    # 6) With date + rib_size_v4 threshold + status=['ready']
    run_vp_query(
        f"List VPs at date={rib_date_str} with rib_size_v4 > 900000 and status=['ready'].",
        **base_kwargs,
        date=rib_date_str,
        rib_size_v4=(">", "900000"),
        status=["ready"],
    )

    # 7) 24h interval using date_end + status=['up','down']
    run_vp_query(
        f"List VPs over a 24h interval: date={rib_date_str} to date_end={date_end_str}, filtered by status=['up','down'].",
        **base_kwargs,
        date=rib_date_str,
        date_end=date_end_str,
        status=["up", "down"],
    )
