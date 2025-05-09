from pybgproutesapi import vantage_points, rib
import os

min_hops = None

for vp in vantage_points(source=["bgproutes.io", "ris"], country=['NL']):
    
    # Get the RIB entries for this VP at the given date and time and with both ASes in the AS path.
    rib_dic = rib([vp['ip']], date="2025-05-09T01:30:11", aspath_regexp='(^| )1853 (|.* )2914($| )|(^| )2914 (|.* )1853($| )')

    # Iterate over all entries in the rib.
    for aspath, community in rib_dic[vp['ip']].values():
        # Transform string ASpath into list of integers.
        aspath = [int(asn) for asn in aspath.split(' ')]

        # Calculate the hop count
        hop_count = abs(aspath.index(1853) - aspath.index(2914))
                
        # Update the min hop count if needed
        if min_hops is None or hop_count < min_hops:
            min_hops = hop_count

print('min_hops: ', min_hops)