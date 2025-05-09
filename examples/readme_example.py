from pybgproutesapi import vantage_points, updates, rib

# Get vantage points in FR or US from RIS or PCH
vps = vantage_points(
    source=["ris", "pch"],
    country=["FR", "US"]
)
print (vps)

# Get updates from a VP during a 1-hour window
for update in updates(
    vp_ip="178.208.11.4",
    start_date="2025-05-09T10:00:00",
    end_date="2025-05-09T11:00:00",
    aspath_regexp=" 6830 "):
    
    print (update)

# Get RIB entries for a specific VP and for all prefixes contained in 8.0.0.0/8.
rib_data = rib(
    vp_ips=["187.16.217.110"],
    date='2025-05-09T20:00:00',
    return_community=False,
    prefix_filter=[('<<', '8.0.0.0/8')])

for prefix, (aspath, community) in rib_data["187.16.217.110"].items():
    print(prefix, aspath, community)
