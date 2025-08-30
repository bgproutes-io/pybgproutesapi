from pybgproutesapi import vantage_points, rib
from datetime import datetime, timedelta

# Compute yesterday's date at 01:30:11 UTC
rib_date = (datetime.utcnow() - timedelta(days=1)).replace(hour=1, minute=30, second=11, microsecond=0)
rib_date_str = rib_date.strftime("%Y-%m-%dT%H:%M:%S")

min_hops = None

vps = vantage_points(
    sources=["bgproutes.io", "ris"],
    country=['NL'],
    date=rib_date_str,
)

# To avoid excessive resource usage and triggering rate limits, we intentionally focus on just 10 VPs in this example.
for vp in vps[:10]:
    
    # Let's just print the vantage point, to follow the progress.
    print(vp)

    # Get the RIB entries for this VP at the given date and time and with both ASes in the AS path.
    rib_dic = rib(vp, date=rib_date_str, aspath_regexp='(^| )1853 (|.* )2914($| )|(^| )2914 (|.* )1853($| )')

    # Iterate over all entries in the rib.
    for aspath, community in rib_dic[vp.peering_protocol][str(vp.id)].values():
        # Transform string ASpath into list of integers.
        aspath = [int(asn) for asn in aspath.split(' ')]

        # Calculate the hop count
        hop_count = abs(aspath.index(1853) - aspath.index(2914))
                
        # Update the min hop count if needed
        if min_hops is None or hop_count < min_hops:
            min_hops = hop_count

print('min_hops: ', min_hops)