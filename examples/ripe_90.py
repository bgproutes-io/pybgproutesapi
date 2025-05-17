from pybgproutesapi import vantage_points, updates

# To avoid excessive resource usage and triggering rate limits, we intentionally focus on just 10 VPs in this example.
vps = vantage_points(source=["routeviews"])[:10]

i = 0
for vp in vps:
    vp_upd = updates(
        vp_ip=vp,
        start_date="2025-05-13T00:00:00",
        end_date="2025-05-14T00:00:00",
        aspath_regexp="^3333 | 3333 | 3333$"
    )

    print (i, len(vps), vp, vp_upd)
    i += 1