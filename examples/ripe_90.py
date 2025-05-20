from pybgproutesapi import vantage_points, updates
from datetime import datetime, timedelta

# Define date range: yesterday 00:00:00 to today 00:00:00
end_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
start_date = end_date - timedelta(days=1)

start_str = start_date.strftime("%Y-%m-%dT%H:%M:%S")
end_str = end_date.strftime("%Y-%m-%dT%H:%M:%S")

# To avoid excessive resource usage and triggering rate limits, we intentionally focus on just 10 VPs in this example.
vps = vantage_points(source=["routeviews"])[:10]

i = 0
for vp in vps:
    vp_upd = updates(
        vp_ip=vp,
        start_date=start_str,
        end_date=end_str,
        aspath_regexp="^3333 | 3333 | 3333$"
    )

    print(i, len(vps), vp, vp_upd)
    i += 1