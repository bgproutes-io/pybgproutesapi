from pybgproutesapi import vantage_points, updates, rib, format_updates_response, format_rib_response, chunked, merge_responses
from datetime import datetime, timedelta

# Use current day minus one day
yesterday = datetime.utcnow() - timedelta(days=1)
start_time = yesterday.replace(hour=20, minute=0, second=0, microsecond=0)
end_time = yesterday.replace(hour=21, minute=0, second=0, microsecond=0)

# Format in ISO 8601
start_date_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
end_date_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")

vps = vantage_points(
    date=start_date_str,
)

vps = vantage_points(
    sources=["ris", "pch"],
    countries=["FR", "CH"],
    date=start_date_str,
    date_end=end_date_str
)

vps = vantage_points(
    date=start_date_str,
    return_uptime_intervals=True
)
