from datetime import datetime, timedelta
from pybgproutesapi import vantage_points, topology

# Use current day minus one day
yesterday = datetime.utcnow() - timedelta(days=1)
date = yesterday.replace(hour=20, minute=0, second=0, microsecond=0)
date_str = date.strftime("%Y-%m-%d")

# Get all vantage points in a french network.
vps = vantage_points(source=["ris", "routeviews", "bgproutes.io", "pch", "cgtf"], country=['FR'])

print(f"Total vantage points: {len(vps)}")

# Store unique AS links (as tuples)
all_links = set()

# Store unique AS paths
all_aspaths = set()

# Process in batches of 10
batch_size = 50
for i in range(0, len(vps), batch_size):
    batch = vps[i:i + batch_size]
    print(f"Processing batch {i // batch_size + 1} with {len(batch)} VPs...")
    
    try:
        topo = topology(batch, date_str, with_aspath=False, with_updates=False, with_rib=True)
        
        # Normalize links as tuples of integers
        for link in topo["links"]:
            all_links.add(tuple(link))
        
        all_aspaths.update(topo['aspaths'])
    except Exception as e:
        print(f"Error processing batch {i // batch_size + 1}: {e}")

# Return total count of distinct links
print(f"Total distinct AS links: {len(all_links)}")

# Return total count of distinct links
print(f"Total distinct AS aspaths: {len(all_aspaths)}")
