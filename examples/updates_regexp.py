from pybgproutesapi import vantage_points, updates, rib
from datetime import datetime, timedelta

# Define date range: yesterday between 10:00 and 20:00 UTC
yesterday = datetime.utcnow() - timedelta(days=1)
start_date = yesterday.replace(hour=10, minute=0, second=0, microsecond=0)
end_date = yesterday.replace(hour=20, minute=0, second=0, microsecond=0)

start_str = start_date.strftime("%Y-%m-%dT%H:%M:%S")
end_str = end_date.strftime("%Y-%m-%dT%H:%M:%S")

# Retrieve the full feeders in an FR or US ASN and operated by RIS or bgproutes.io.
vps = vantage_points(
    source=["bgproutes.io", "ris"],
    country=["FR", "US"],
    rib_size_v4=('>', '900000')
)

# To avoid excessive resource usage and triggering rate limits, we intentionally focus on just 10 VPs in this example.
for vp in vps[:10]:
    nb_upd = updates(
        vp,
        start_date=start_str,
        end_date=end_str,
        return_count=True,
        aspath_regexp=' 3333 '
    )

    print(vp['ip'], nb_upd)