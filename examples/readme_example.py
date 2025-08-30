from pybgproutesapi import vantage_points, updates, rib, format_updates_response, format_rib_response
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
    sources=["ris", "pch"],
    countries=["FR", "US"],
    date=start_date_str,
    date_end=end_date_str
)

response = updates(
    vps,
    start_date=start_date_str,
    end_date=end_date_str,
    aspath_regexp=" 6830 "
)

print(format_updates_response(response))

# Get RIB entries for a specific VP and for all prefixes contained in 8.0.0.0/8
response = rib(
    vps,
    date=rib_date_str,
    return_community=False,
    prefix_filter=[('<<', '8.0.0.0/8')]
)

print(format_rib_response(response))