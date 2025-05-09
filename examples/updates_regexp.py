from pybgproutesapi import vantage_points, updates, rib
import os

# Retrieve the full feeders in an FR or US ASN and operated by RIS or bgproutes.io.
vps = vantage_points(
    source=["bgproutes.io", "ris"],
    country=["FR", "US"],
    rib_size_v4=('>', '900000')
)

for vp in vps:
    nb_upd = updates(vp,
        start_date="2025-05-08T10:00:00",
        end_date="2025-05-08T20:00:00",
        return_count=False,
        aspath_regexp=' 3333 '
    )

    print (vp['ip'], nb_upd)

