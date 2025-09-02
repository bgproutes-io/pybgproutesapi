from pybgproutesapi import vantage_points, updates, rib, format_updates_response, format_rib_response, chunked, merge_responses
from datetime import datetime, timedelta

# Use current day minus one day
yesterday = datetime.utcnow() - timedelta(days=1)
start_time = yesterday.replace(hour=20, minute=0, second=0, microsecond=0)
end_time = yesterday.replace(hour=21, minute=0, second=0, microsecond=0)
rib_time = yesterday.replace(hour=22, minute=0, second=0, microsecond=0)

# Format in ISO 8601
start_date_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
end_date_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")
rib_date_str = rib_time.strftime("%Y-%m-%dT%H:%M:%S")

# Get vantage points in FR or US from RIS or PCH
vps = vantage_points(
    sources=["ris", "pch"],
    countries=["FR", "CH"],
    date=start_date_str,
    date_end=end_date_str
)

print (f'A total of {len(vps)} VPs have been found.')

# --- UPDATES: run by batches of 10 VPs ------------------------------------
updates_merged = {"bgp": {}, "bmp": {}}
for batch in chunked(vps, 10):
    resp = updates(
        batch,
        start_date=start_date_str,
        end_date=end_date_str,
        aspath_regexp=" 6830 "
    )
    updates_merged = merge_responses(updates_merged, resp)

print(format_updates_response(updates_merged))

# --- RIB: run by batches of 10 VPs ----------------------------------------
rib_merged = {"bgp": {}, "bmp": {}}
for batch in chunked(vps, 10):
    resp = rib(
        batch,
        date=rib_date_str,
        return_community=False,
        prefix_filter=[('<<', '8.0.0.0/8')]
    )
    rib_merged = merge_responses(rib_merged, resp)

print(format_rib_response(rib_merged))
