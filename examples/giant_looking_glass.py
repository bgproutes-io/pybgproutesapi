from pybgproutesapi import vantage_points, rib
from datetime import datetime, timedelta

# NOTE: ALREADY UPDATED WITH THE NEW BMP CODE VERSION, ALL OTHER EXAMPLES ARE NOT UPDATED.

# Compute yesterday's date at 10:30:00 UTC
rib_date = (datetime.utcnow() - timedelta(days=0)).replace(hour=10, minute=30, second=0, microsecond=0)
rib_date_str = rib_date.strftime("%Y-%m-%dT%H:%M:%S")

# Retrieve the full feeder vantage points operated by RIS or bgproutes.io, routeviews, pch and cgtf.
vps = vantage_points(
    source=['ris', 'bgproutes.io', 'routeviews', 'pch', 'cgtf'],
    rib_size_v4=('>', '900000'),
    date="2024-06-01T12:00:00"
)

ribs = rib(vps,
    date="2024-06-01T12:00:00",
    prefix_exact_match=['65.169.6.0/23', '91.106.223.0/24', '105.77.0.0/16'],
)

for vp_id, entries in ribs['bgp'].items():
    print (vp_id, entries)
    print(f"Vantage Point: {vp_id}")
    for prefix, (aspath, community) in entries.items():
        print(f"\tPrefix: {prefix}")
        print(f"\t\tAS Path: {aspath}")
        print(f"\t\tCommunities: {community}")