# Count distinct AS links and paths in yesterday's topology for selected vantage points.

from datetime import datetime, timedelta, timezone
from pybgproutesapi import vantage_points, topology

# Retrieve topology over yesterday's UTC interval and combine unique
# AS links and AS paths across the first 10 vantage points.
today = datetime.now(timezone.utc).replace(
    hour=0, minute=0, second=0, microsecond=0
)
yesterday = today - timedelta(days=1)

date_str = yesterday.strftime("%Y-%m-%dT%H:%M:%S")
date_end_str = today.strftime("%Y-%m-%dT%H:%M:%S")
vp_date_str = yesterday.replace(hour=20).strftime("%Y-%m-%dT%H:%M:%S")

vps = vantage_points(
    date=vp_date_str,
    sources=["ris", "routeviews", "bgproutes.io", "pch", "cgtf"],
    # countries=["FR"],
)[:10]

print(f"Interval: {date_str} to {date_end_str} UTC")
print(f"Total vantage points: {len(vps)}")

all_links = set()
all_aspaths = set()
failed_batches = 0

batch_size = 50
for i in range(0, len(vps), batch_size):
    batch = vps[i:i + batch_size]
    batch_number = i // batch_size + 1
    print(f"Processing batch {batch_number} with {len(batch)} VPs...")
    print (date_str)
    try:
        topo = topology(
            batch,
            date=date_str,
            with_aspath=True,
            with_updates=True,
            with_rib=True,
            ignore_private_asns=True,
        )

        for as1, as2 in topo["links"]:
            all_links.add((min(as1, as2), max(as1, as2)))

        all_aspaths.update(topo["aspaths"])

    except Exception as e:
        failed_batches += 1
        print(f"Error processing batch {batch_number}: {e}")

if failed_batches:
    print(f"\nResults are incomplete: {failed_batches} batch(es) failed.")

print(f"Total distinct AS links: {len(all_links)}")
print(f"Total distinct AS paths: {len(all_aspaths)}")
