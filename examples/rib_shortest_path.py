from pybgproutesapi import vantage_points, rib
from datetime import datetime, timedelta
import requests  # only used for exception types

# Compute yesterday's date at 22:30:11 UTC
rib_date = (datetime.utcnow() - timedelta(days=1)).replace(hour=22, minute=30, second=11, microsecond=0)
rib_date_str = rib_date.strftime("%Y-%m-%dT%H:%M:%S")

min_hops = None

vps = vantage_points(
    sources=["bgproutes.io"],
    date=rib_date_str,
)

aspath_re = r"(^| )1853 (|.* )2914($| )|(^| )2914 (|.* )1853($| )"

for vp in vps[:100]:
    print(vp)

    try:
        rib_dic = rib(
            vp,
            date=rib_date_str,
            aspath_regexp=aspath_re,
        )
    except (requests.exceptions.HTTPError,
            requests.exceptions.JSONDecodeError,
            requests.exceptions.RequestException,
            Exception) as e:
        # 502 / invalid JSON / network issues / anything unexpected:
        print(f"[WARN] rib() failed for {vp} ({type(e).__name__}): {e}")
        continue

    proto_dic = rib_dic.get(vp.peering_protocol, {})
    vp_dic = proto_dic.get(str(vp.unique_id), {})

    for tup in vp_dic.values():
        aspath_str = tup[0]
        aspath = [int(asn) for asn in aspath_str.split() if asn.isdigit()]

        # Guard: only compute if both ASNs are present
        if 1853 not in aspath or 2914 not in aspath:
            continue

        hop_count = abs(aspath.index(1853) - aspath.index(2914))

        if min_hops is None or hop_count < min_hops:
            min_hops = hop_count

print("min_hops:", min_hops)