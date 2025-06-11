from pybgproutesapi import vantage_points, rib
from datetime import datetime, timedelta

# Compute yesterday's date at 10:30:00 UTC
rib_date = (datetime.utcnow() - timedelta(days=0)).replace(hour=10, minute=30, second=0, microsecond=0)
rib_date_str = rib_date.strftime("%Y-%m-%dT%H:%M:%S")

# Retrieve the full feeder vantage points operated by RIS or bgproutes.io, routeviews, pch and cgtf.
vps = vantage_points(
    source=['ris', 'bgproutes.io', 'routeviews', 'pch', 'cgtf'],
    rib_size_v4=('>', '900000')
)

ribs = rib(vps,
    date=rib_date_str,
    prefix_exact_match=['65.169.6.0/23', '91.106.223.0/24', '105.77.0.0/16'],
)

for vp_ip, entries in ribs.items():
    print(f"Vantage Point: {vp_ip}")
    if 'details' in entries:
        print(f"\t{entries}")  # e.g., "The vantage point was down"
    else:
        for prefix, (aspath, community) in entries.items():
            print(f"\tPrefix: {prefix}")
            print(f"\t\tAS Path: {aspath}")
            print(f"\t\tCommunities: {community}")