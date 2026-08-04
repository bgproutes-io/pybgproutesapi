from pybgproutesapi import vantage_points, rib, format_rib_response
from datetime import datetime, timedelta, timezone

# Compute today's date at 10:30:00 UTC
rib_date = (datetime.now(timezone.utc) - timedelta(days=1)).replace(hour=10, minute=30, second=0, microsecond=0)
rib_date_str = rib_date.strftime("%Y-%m-%dT%H:%M:%S")

# Retrieve the full feeder vantage points operated by RIS or bgproutes.io, routeviews, pch and cgtf.
vps = vantage_points(
    # sources=['ris', 'bgproutes.io', 'routeviews', 'pch', 'cgtf'],
    # rib_size_v4=('>', '900000'),
    date=rib_date_str,
    peering_protocol='bmp',
    # ixp_ids=[31],
    ixp_names=['DE-CIX Frankfurt'],
    ixp_is_rs=True,
    return_status_history=True,
    return_metadata=True
)


for vp in vps:
    print (vp)
    print (vp.metadata)
    print (vp.ixp_name)
    print (vp.rib_size_v4_per_feed)
    print (vp.rib_size_v6_per_feed)

