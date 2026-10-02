# Retrieve DE-CIX Frankfurt BMP vantage points for yesterday at 10:30 UTC.
# For each one, print metadata and RIB sizes, then list Downstream Invalid
# ASPA routes with their prefixes and AS paths. Report unavailable RIBs.
# The API automatically selects the available BMP feed with the lowest feed ID.

from datetime import datetime, timedelta, timezone
from pprint import pformat

from pybgproutesapi import vantage_points, rib


def pretty(value):
    return pformat(value, indent=4, width=100, sort_dicts=False)


# Compute yesterday's date at 10:30:00 UTC.
rib_date = (datetime.now(timezone.utc) - timedelta(days=1)).replace(
    hour=10, minute=30, second=0, microsecond=0
)
rib_date_str = rib_date.strftime("%Y-%m-%dT%H:%M:%S")

# Retrieve BMP vantage points from DE-CIX Frankfurt route servers.
vps = vantage_points(
    date=rib_date_str,
    peering_protocol="bmp",
    ixp_names=["DE-CIX Frankfurt"],
    ixp_is_rs=True,
    return_status_history=True,
    return_metadata=True,
)

print(f"RIB snapshot: {rib_date_str} UTC")
print(f"Total vantage points: {len(vps)}")

for index, vp in enumerate(vps, start=1):
    vp_id = str(vp.unique_id)

    print(f"\n{'=' * 80}")
    print(f"Vantage point {index} — ID: {vp_id}")
    print("=" * 80)
    print(f"VP: {vp}")
    print(f"IXP: {vp.ixp_name}")
    print(f"\nMetadata:\n{pretty(vp.metadata)}")
    print(f"\nIPv4 RIB sizes per feed:\n{pretty(vp.rib_size_v4_per_feed)}")
    print(f"\nIPv6 RIB sizes per feed:\n{pretty(vp.rib_size_v6_per_feed)}")

    # Retrieve Downstream Invalid routes, including their AS paths.
    response = rib(
        vps=vp,
        date=rib_date_str,
        aspa_status_filter=["D-I"],
        return_aspath=True,
        return_community=False,
        return_aspa_status=False,
        return_rov_status=False,
        details=True,
    )

    bmp_data = response.get("data", {}).get("bmp", {})
    feed_statuses = response.get("info", {}).get("bmp", {}).get(vp_id, {})

    # The API reports ready feeds as "up".
    rib_available = (
        vp_id in bmp_data
        or (
            isinstance(feed_statuses, dict)
            and "up" in feed_statuses.values()
        )
    )

    print(f"\nFeed status: {pretty(feed_statuses)}")

    if not rib_available:
        print("Downstream Invalid routes: unavailable (RIB not ready)")
        continue

    invalid_routes = bmp_data.get(vp_id, {})
    print(f"Downstream Invalid routes: {len(invalid_routes):,}")

    if invalid_routes:
        print(f"\n{'Prefix':<43} AS path")
        print("-" * 80)

        for prefix, entry in sorted(invalid_routes.items()):
            as_path = entry[0]
            print(f"{prefix:<43} {as_path}")
