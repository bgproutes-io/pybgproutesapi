# Public API Client Documentation

This document describes the public `pybgproutesapi` Python wrappers. All functions accept:

- `base_url`: optional API origin, defaulting to `https://api.bgproutes.io`.
- `api_key`: optional API key. If omitted, `BGP_API_KEY` is read from the environment.
- `details`: default `False`. If `False`, functions return the API `data` field only. If `True`, functions return the full API envelope with `seconds`, `bytes`, optional `info`, and `data`.

List arguments may be passed as Python lists or as already-comma-separated strings. Prefix filters may be passed as `[("<<", "203.0.113.0/24")]` or as `"<<:203.0.113.0/24"`.

Live test note: against `production_testing` (`http://192.168.130.1:8080`, API key `test`), `vantage_points`, `updates`, `rib`, `topology`, and `messages` passed smoke tests with BMP VP `1`. The `/monitoring` server endpoint returned HTTP 500 because that deployment passed no usable DB helper to the monitoring handler; the client wrapper still matches the API contract.

## `vantage_points(...)`

Wraps `GET /v1/vantage_points` and returns a list of `VPBGP`/`VPBMP` objects, or a detailed envelope with parsed objects under `data`.

Important arguments:

| Argument | Type | Description |
|---|---|---|
| `vp_bgp_ids`, `vp_bmp_ids` | list/string | Filter by VP IDs. |
| `vp_ips`, `vp_asns` | list/string | Filter by VP IPs or ASNs. |
| `peering_protocol` | string/list | `bgp`, `bmp`, or omitted. |
| `bmp_parent_ips`, `bmp_parent_asns` | list/string | BMP parent filters. |
| `date`, `date_end` | string | UTC `YYYY-MM-DDTHH:MM:SS`. |
| `data_afi` | int | `4`, `6`, or `None`. |
| `sources`, `countries`, `org_countries` | list/string | Metadata filters. |
| `rib_size_v4`, `rib_size_v6` | tuple | Operator/value tuple, e.g. `(">", 900000)`. |
| `status` | list/string | Status filter. |
| `return_status_history` | bool | Include status history. |
| `return_rib_history` | bool | Include recent RIB origin/difference history. |
| `rib_status` | bool | Include RIB history completeness/corruption notes. |

Returned objects expose `unique_id` and compatibility property `id`, plus `ip`, `asn`, `peering_protocol`, RIB sizes, status fields, and BMP parent/feed fields on `VPBMP`.

## `updates(vps, start_date, end_date, ...)`

Wraps `/v1/updates`. `vps` is one VP object or a list of `VPBGP`/`VPBMP`. The wrapper sends GET for small queries and POST for large VP or exact-match lists.

Key arguments: `bmp_feed_type`, `return_count`, `data_afi`, `max_updates_to_return`, `type_filter`, `prefix_filter`, `prefix_exact_match`, `return_aspath`, `aspath_exact_match`, `aspath_regexp`, `return_community`, `community_regexp`, `chronological_order`, `return_rov_status`, `return_aspa_status`, `rov_status_filter`, `aspa_status_filter`.

Return with `details=False` and `return_count=False`:

```python
{
    "bgp": {1: [[timestamp, "A", prefix, aspath, community, aspa, rpki, -1]]},
    "bmp": {16: [[timestamp, "A", prefix, aspath, community, aspa, rpki, feed_type_id]]},
}
```

Return with `return_count=True`:

```python
{"bgp": {1: {"A": 10, "W": 2}}, "bmp": {16: {"A": 5, "W": 1}}}
```

## `rib(vps, date, ...)`

Wraps `/v1/rib`. `vps` is one VP object or a list.

Key arguments: `bmp_feed_type`, `data_afi`, `prefix_filter`, `prefix_exact_match`, `return_aspath`, `aspath_exact_match`, `aspath_regexp`, `return_community`, `community_regexp`, `return_count`, `return_rov_status`, `return_aspa_status`, `rov_status_filter`, `aspa_status_filter`.

Return with `details=False` and `return_count=False`:

```python
{
    "bgp": {1: {"203.0.113.0/24": [aspath, community, aspa, rpki, -1]}},
    "bmp": {16: {"203.0.113.0/24": [aspath, community, aspa, rpki, feed_type_id]}},
}
```

Return with `return_count=True`:

```python
{"bgp": {1: 900000}, "bmp": {16: 899000}}
```

## `topology(vps, date, ...)`

Wraps `/v1/topology`. `date` may be `YYYY-MM-DDTHH:MM:SS` or `YYYY-MM-DD`.

Key arguments: `date_end`, `data_afi`, `bmp_feed_type`, `directed`, `with_aspath`, `with_updates`, `with_rib`, `as_to_ignore`, `ignore_private_asns`.

Return:

```python
{"links": [[64500, 64496]], "aspaths": [[64500, 64496, 64497]]}
```

## `messages(vps, start_date, end_date, ...)`

Wraps `GET /v1/messages`. `vps` is one VP object or a list.

Arguments: `interval_time`, `prefix_filter`, `prefix_exact_match`, `aspath_regexp`, `aspath_exact_match`, `community_regexp`, `rov_status_filter`, `aspa_status_filter`, `bmp_visibility`.

Return:

```python
[
    [1, "bgp", [[received_updates, received_withdraws], ...]],
    [16, "bmp", [[received_prefixes, received_withdraws, filtered_received_prefixes, filtered_received_withdraws, announced_prefixes, announced_withdraws, filtered_announced_prefixes, filtered_announced_withdraws], ...]],
]
```

## `monitoring(start_date, end_date, ...)`

Wraps `GET /v1/monitoring`.

Arguments: `bmp_parent_ips`, `bmp_parent_asns`, `frequency`.

Return without `frequency` is intended to be a dict keyed by `"bmp_parent_asn,bmp_parent_ip"`. Return with `frequency` is keyed first by bucket start timestamp, then by session key.

Live test caveat: `production_testing` currently returns a server error for this endpoint because the deployment's monitoring DB helper is `None`.
