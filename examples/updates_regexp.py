from pybgproutesapi import vantage_points, updates, format_updates_response, chunked, merge_responses
from datetime import datetime, timedelta

# Define date range: yesterday between 10:00 and 20:00 UTC
yesterday = datetime.utcnow() - timedelta(days=1)
start_date = yesterday.replace(hour=10, minute=0, second=0, microsecond=0)
end_date = yesterday.replace(hour=20, minute=0, second=0, microsecond=0)

start_str = start_date.strftime("%Y-%m-%dT%H:%M:%S")
end_str = end_date.strftime("%Y-%m-%dT%H:%M:%S")

# Retrieve the full feeders in an FR or US ASN and operated by RIS or bgproutes.io.
vps = vantage_points(
    sources=["bgproutes.io", "ris"],
    countries=["FR", "US"],
    rib_size_v4=('>', '900000')
)[:10]

# To avoid excessive resource usage and triggering rate limits, we intentionally focus on just 10 VPs in this example.
updates_merged = {"bgp": {}, "bmp": {}}
for batch in chunked(vps, 2):
    response = updates(
        batch,
        start_date=start_str,
        end_date=end_str,
        return_count=True,
        aspath_regexp=' 3333 '
    )
    updates_merged = merge_responses(updates_merged, response)

print(format_updates_response(updates_merged))
