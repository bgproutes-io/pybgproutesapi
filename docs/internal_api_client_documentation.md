# Internal API Client Documentation

These wrappers require an API deployment where `IS_DEPLOYED_INTERNALLY=True`.

All functions accept `base_url`, `api_key`, and `details` like the public wrappers. With `details=False`, only the API `data` field is returned. With `details=True`, the full envelope is returned.

Live test note: against `production_testing` (`http://192.168.130.1:8080`, API key `test`), all three wrappers passed smoke tests with BMP VP `1`.

## `bmp_rib_with_status(vp, date, ...)`

Wraps `/v1/bmp_rib_with_status`. `vp` may be a `VPBMP` object or an integer BMP VP ID.

Arguments:

| Argument | Type | Default | Description |
|---|---|---:|---|
| `vp` | `VPBMP`/int | required | BMP VP object or ID. |
| `date` | string | required | UTC datetime or epoch accepted by API. |
| `visibility` | string | `all` | `all`, `filtered_only`, `accepted_only`, `withdrawn_only`. |
| `data_afi` | int | `None` | `4`, `6`, or `None`. |
| `prefix_filter` | list/string | `None` | Prefix filter clauses. |
| `prefix_exact_match` | list/string | `None` | Exact prefixes. |
| `aspath_regexp`, `aspath_exact_match` | string/list | `None` | AS-path filters. |
| `community_regexp` | string | `None` | Community regex. |
| `return_aspath`, `return_community` | bool | `True` | Include route attributes. |
| `return_rov_status`, `return_aspa_status` | bool | `True` | Include RPKI/ASPA statuses. |
| `rov_status_filter`, `aspa_status_filter` | list/string | `None` | Status filters using API codes. |
| `start_index`, `stop_index` | int | `None` | Optional API index window. |

Return row shape:

```python
[
    prefix,
    [aspath_pre, aspath_post],
    [community_pre, community_post],
    [local_pref_pre, local_pref_post],
    [med_pre, med_post],
    [nexthop_pre, nexthop_post],
    [origin_pre, origin_post],
    [real_timestamp_pre, real_timestamp_post],
    [aspa_pre, aspa_post],
    rpki,
    filtered_reason,
    status,
]
```

Live caveat: exact-prefix filters reliably produce small responses. On `production_testing`, `start_index=0&stop_index=5` returned more than five rows, matching the server-side behavior.

## `bmp_updates_for_analysis(vp, start_date, end_date, ...)`

Wraps `/v1/bmp_updates_for_analysis`. `vp` may be a `VPBMP` object or integer BMP VP ID.

Arguments include `adj_rib_type` (`"in"`, `"out"`, or `None` for both), `visibility`, `data_afi`, `chronological_order`, `max_updates_to_return`, prefix/AS-path/community filters, and RPKI/ASPA return/filter flags.

Return:

```python
{
    "in": [
        [timestamp, update_type, prefix, aspath_pair, community_pair, local_pref_pair, med_pair, nexthop_pair, origin_pair, real_timestamp_pair, aspa_pair, rpki, filtered_reason, status]
    ],
    "out": []
}
```

If `adj_rib_type="in"`, only the `"in"` key is returned; if `"out"`, only `"out"` is returned.

## `route_propagation_path(received_vp, prefix, timestamp, aspath, ...)`

Wraps `/v1/route_propagation_path`. `received_vp` may be a `VPBMP` object or integer BMP VP ID.

Arguments: `communities`, `nexthop`, `local_pref`, `med`, `max_depth`.

Return:

```python
{
    "nodes": [
        {"id": 0, "router_id": "7.151.0.1", "router_ip": "179.0.77.7", "router_asn": 7}
    ],
    "edges": [
        {
            "from": 0,
            "to": 1,
            "prefix": "1.0.0.0/24",
            "timestamp_recv": 1782325500,
            "timestamp_sent": 1782325500,
            "aspath_recv": "1 2",
            "aspath_sent": "1 2"
        }
    ],
}
```

Every edge has `from` and `to`; additional edge attributes are whatever the API graph returns.
