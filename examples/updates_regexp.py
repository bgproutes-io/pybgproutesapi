from pybgproutesapi import vantage_points, updates, rib

# Retrieve the full feeders in an FR or US ASN and operated by RIS or bgproutes.io.
vps = vantage_points(
    source=["bgproutes.io", "ris"],
    country=["FR", "US"],
    rib_size_v4=('>', '900000')
)

# To avoid excessive resource usage and triggering rate limits, we intentionally focus on just 10 VPs in this example.
for vp in vps[:10]:
    nb_upd = updates(vp,
        start_date="2025-05-11T10:00:00",
        end_date="2025-05-11T20:00:00",
        return_count=True,
        aspath_regexp=' 3333 '
    )

    print (vp['ip'], nb_upd)

