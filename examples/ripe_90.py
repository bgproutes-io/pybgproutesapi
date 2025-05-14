from pybgproutesapi import vantage_points, updates

vps = vantage_points(source=["routeviews"])

for vp in vps:
    vp_upd = updates(
        vp_ip=vp,
        start_date="2025-05-14T00:00:00",
        end_date="2025-05-15T00:00:00",
        aspath_regexp="^3333 | 3333 | 3333$"
    )

    print (len(vps), vp, vp_upd)
