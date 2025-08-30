from pybgproutesapi import vantage_points, topology
from datetime import datetime, timedelta
from more_itertools import chunked
import networkx as nx

# Compute yesterday's date (only the day part is used for topology API)
rib_date = (datetime.utcnow() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
rib_date_str = rib_date.strftime("%Y-%m-%dT%H:%M:%S")

# Retrieve VPs with large RIBs from RIS or bgproutes.io
vps = vantage_points(
    sources=['ris', 'bgproutes.io'],
    rib_size_v4=('>', '900000'),
    date=rib_date_str
)

# WARNING: This line speeds up the processing, but DO NOT FORGET to remove the line if you want complete data.
vps = vps[:30]

# Initialize empty graph
G = nx.Graph()

# Process in batches of 10
for vp_batch in chunked(vps, 10):
    print(f"\n📦 Processing the following VPs: {', '.join(map(lambda x: f"Protocol: {x.peering_protocol}, ID: {x.id}", vp_batch))}")

    # Get topology for this batch of VPs
    topo = topology(vp_batch, date=rib_date_str, with_rib=True, with_updates=False)

    # Add edges to the graph from the topology data
    for as1, as2 in topo['links']:
        G.add_edge(as1, as2)

# Identify ASes that are single-homed to AS5511
neighbors = [asn for asn in G.neighbors(5511)]
single_homed = [asn for asn in G.neighbors(5511) if G.degree[asn] == 1]

print (f"\n✅ Found {len(neighbors)} neighbors ASes of AS5511")
print (f"\n✅ Found {len(single_homed)} single-homed ASes of AS5511")
print (single_homed)