from pybgproutesapi import vantage_points, rib, format_rib_response
from datetime import datetime, timedelta, timezone

# Compute today's date at 10:30:00 UTC
rib_date = (datetime.now(timezone.utc) - timedelta(days=1)).replace(hour=10, minute=30, second=0, microsecond=0)
rib_date_str = rib_date.strftime("%Y-%m-%dT%H:%M:%S")

# Retrieve the full feeder vantage points operated by RIS or bgproutes.io, routeviews, pch and cgtf.
vps = vantage_points(
    sources=['ris', 'bgproutes.io', 'routeviews', 'pch', 'cgtf'],
    rib_size_v4=('>', '900000'),
    date=rib_date_str,
)

# Get the ribs at the specified time.
response = rib(vps,
    date=rib_date_str,
    prefix_exact_match=['65.169.6.0/23', '91.106.223.0/24', '105.77.0.0/16'],
    return_rov_status=True,
    return_aspa_status=True
)

print (format_rib_response(response))
