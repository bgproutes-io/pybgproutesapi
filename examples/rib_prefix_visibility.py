from pybgproutesapi import vantage_points, rib
import os

# Retrieve the vantage points operated by RIS or bgproutes.io.
vps = vantage_points(
    source=["ris", 'bgproutes.io'],
)

ribs = rib(vps,
    date="2025-05-09T1:30:00",
    prefix_exact_match=['65.169.6.0/23', '91.106.223.0/24', '105.77.0.0/16'],
)

for vp_ip, entries in ribs.items():
    print(f"Vantage Point: {vp_ip}")
    if 'details' in entries:
        print(f"\t{entries}")  # e.g., "The vantage point was down"
    else:
        for prefix, (aspath, community) in entries.items():
            print(f"\tPrefix: {prefix}")
            print(f"\t\tAS Path: {aspath}")
            print(f"\t\tCommunities: {community}")