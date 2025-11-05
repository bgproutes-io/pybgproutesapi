import random
from datetime import datetime, timedelta

from pybgproutesapi import (
    vantage_points,
    updates,
    chunked,
)

# Use current day minus one day
yesterday = datetime.utcnow() - timedelta(days=1)

# Pick a number between 0 and 23 (included) randomly, and use that number as the hour below
hour = random.randint(0, 23)
start_time = yesterday.replace(hour=hour, minute=0, second=0, microsecond=0)
end_time = yesterday.replace(hour=hour, minute=2, second=0, microsecond=0)

# Format in ISO 8601
start_date_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
end_date_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")

# Get vantage points in FR or US from RIS or PCH
vps = vantage_points(
    date=start_date_str,
    date_end=end_date_str,
    rib_size_v4=('>', '900000'),
    data_afi=4
)

random.shuffle(vps)
vps = vps[: min(10, len(vps))]

# --- UPDATES: run by batches of 10 VPs ------------------------------------
updates_merged = {"bgp": {}, "bmp": {}}
for batch in chunked(vps, 1):
    print (batch)
    try:
        resp = updates(
            batch,
            start_date=start_date_str,
            end_date=end_date_str,
            return_count=True,
            exact_prefix_match=['130.79.0.0/16', '65.169.6.0/23', '91.106.223.0/24', '105.77.0.0/16'],
            data_afi=4
        )
    except:
        print ('error (perhaps timeout?)')