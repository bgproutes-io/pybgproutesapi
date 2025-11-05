
import random
from datetime import datetime, timedelta

from pybgproutesapi import (
    vantage_points,
    rib,
    chunked,
)

# Use current day minus one day
yesterday = datetime.utcnow() - timedelta(days=1)

# Pick a number between 0 and 23 (included) randomly, and use that number as the hour below
hour = random.randint(0, 23)
start_time = yesterday.replace(hour=hour, minute=0, second=0, microsecond=0)

# Format in ISO 8601
start_date_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")

# Get vantage points in FR or US from RIS or PCH
vps = vantage_points(
    date=start_date_str,
    rib_size_v4=('>', '900000'),
    data_afi=4
)

random.shuffle(vps)
vps = vps[: min(50, len(vps))]

# --- RIB: run by batches of 10 VPs ----------------------------------------
rib_merged = {"bgp": {}, "bmp": {}}
for batch in chunked(vps, 10):
    resp = rib(
        batch,
        date=start_date_str,
        prefix_filter=[('<<', '8.0.0.0/8')]
    )

