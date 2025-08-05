#/usr/bin/env python

# Copyright 2025 Alarig Le Lay <alarig@swordarmor.fr>
# Code revised by Thomas Holterbach to support pulling data from bgproutes.io with the pybgproutesapi library.
# Distributed under the terms of the GNU General Public License v3

import argparse
import configparser
import datetime
import ipaddress
import logging
import os
import pathlib
import re
import sys

from pybgproutesapi import vantage_points, rib

argp = argparse.ArgumentParser(description=__doc__)
argp.add_argument(
    '-a', '--afi', metavar='str', default='ipv4',
    help='AFI in which we count the route (IPv4 or IPv6)'
)
argp.add_argument(
    '-c', '--config', metavar='str', default='count-as-cone-routes.ini',
    help='INI file to read the config from'
)
argp.add_argument(
    '-d', '--debug', action='count', default=0,
    help='debug logging to /tmp/count-as-cone-routes.log'
)

argp.add_argument('asn')
args = argp.parse_args()
if (args.debug):
    logging.basicConfig(
        filename='/tmp/count-as-cone-routes.log',
        encoding='utf-8',
        format='%(asctime)s %(message)s',
        level=logging.DEBUG
    )

_log = logging.getLogger(os.path.basename(__file__))

config = configparser.ConfigParser()
config.read(args.config)

api_endpoint    = config['bgproutes.io']['endpoint']
api_key         = config['bgproutes.io']['key']

api_req_headers = {
    'accept':       'application/json',
    'x-api-key':    api_key,
}

vantage_points_sources  = ('bgproutes.io', 'pch' , 'ris', 'routeviews', 'cgtf')
vantage_points_asns     = (701, 1299, 2914, 3257, 3320, 3356, 3491, 5511, 6453,
                            6461, 6762, 6830, 7018, 12956)
                            # basically all T1 that I can think of this late

def route_count(afi, asn):
    afi = afi.lower()

    if args.asn in vantage_points_asns:
        _log.info('We have a query about a T1, empty reply for now')
        return 0

    try:
        if afi == 'ipv4':
            req_vantage_points = vantage_points(
                source=vantage_points_sources,
                vp_asns=vantage_points_asns,
                ip_protocol='ipv4')

        elif afi == 'ipv6':
            req_vantage_points = vantage_points(
                source=vantage_points_sources,
                vp_asns=vantage_points_asns,
                ip_protocol='ipv6')

        else:
            _log.error(f'Invalid AFI {afi} given, only IPv4 and IPv6 are supported.')
            sys.exit(1)
    except Exception as e:
        _log.error(f'https://{api_endpoint}/vantage_point for returned error: {e}')
        sys.exit(1)

    vantage_points_list = []
    for point in req_vantage_points:
        vantage_points_list.append(point['ip'])

    route_count = {}
    for vp in vantage_points_list:
        print (f'Processing VP: {vp}')
        try:
            
            tmp = rib(
                vp_ips=[vp],
                date=str(datetime.date.today()) + 'T00:00:00',
                aspath_regexp=f'.*{asn}.*',
                return_count=True)[vp]

            if not isinstance(tmp, dict):
                route_count[vp] = tmp
            else:
                route_count[vp] = 0

        except Exception as e:
            _log.error(f'https://{api_endpoint}/rib for {vp} returned error: {e}')
            continue     

        if route_count[vp] == 0:
            _log.debug(f'{vp} does not see {asn}')

    print (route_count)

    # TODO: to be moved elsewhere, that’s just to test the algorithm
    max_route_count = max(route_count.values())
    if max_route_count < 10:
        max_route_count *= 2
        max_route_count += 10
        return round(max_route_count, -1)
    elif max_route_count < 100:
        max_route_count *= 2
        max_route_count += 10
        return round(max_route_count, -1)
    elif max_route_count < 1000:
        max_route_count *= 1.5
        max_route_count += 100
        return int(round(max_route_count, -2))
    elif max_route_count < 10000:
        max_route_count *= 1.2
        max_route_count += 1000
        return int(round(max_route_count, -3))
    else:
        max_route_count += 10000
        return round(max_route_count, -4)

print(route_count(args.afi, args.asn))
