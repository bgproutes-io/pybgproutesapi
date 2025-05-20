from pybgproutesapi import vantage_points, updates, rib
from datetime import datetime, timedelta

# Use current day minus one day
yesterday = datetime.utcnow() - timedelta(days=1)
start_time = yesterday.replace(hour=10, minute=0, second=0, microsecond=0)
end_time = yesterday.replace(hour=11, minute=0, second=0, microsecond=0)
rib_time = yesterday.replace(hour=20, minute=0, second=0, microsecond=0)

# Format in ISO 8601
start_date_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
end_date_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")
rib_date_str = rib_time.strftime("%Y-%m-%dT%H:%M:%S")

# Get vantage points in FR or US from RIS or PCH
vps = vantage_points(
    source=["ris", "pch"],
    country=["FR", "US"]
)
print(vps)

# Get updates from a VP during a 1-hour window
for update in updates(
    vp_ip="178.208.11.4",
    start_date=start_date_str,
    end_date=end_date_str,
    aspath_regexp=" 6830 "
):
    print(update)

# Get RIB entries for a specific VP and for all prefixes contained in 8.0.0.0/8
rib_data = rib(
    vp_ips=["187.16.217.110"],
    date=rib_date_str,
    return_community=False,
    prefix_filter=[('<<', '8.0.0.0/8')]
)

for prefix, (aspath, community) in rib_data["187.16.217.110"].items():
    print(prefix, aspath, community)