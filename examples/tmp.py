from pybgproutesapi import vantage_points, updates, rib

vps = vantage_points(source=["routeviews"], ip_protocol=4)

r = rib(vps, 
    date="2025-05-10T00:40:00",
    prefix_exact_match=['77.72.40.0/21'])

for vp_ip, r in r.items():
    print (vp_ip, r)
