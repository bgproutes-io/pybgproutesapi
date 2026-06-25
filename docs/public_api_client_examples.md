# Public API Client Examples

Use `base_url="http://192.168.130.1:8080"` and `api_key="test"` to run the live-test examples on `production_testing`.

```python
from pybgproutesapi import vantage_points, updates, rib, topology, messages, monitoring

BASE_URL = "https://api.bgproutes.io"
API_KEY = None  # or set BGP_API_KEY in the environment
```

## Find BMP Vantage Points

```python
vps = vantage_points(
    vp_bmp_ids=[1],
    return_rib_history=True,
    rib_status=True,
    base_url=BASE_URL,
    api_key=API_KEY,
)
vp = vps[0]
print(vp.id, vp.ip, vp.bmp_feed_types)
print(vp.rib_history, vp.rib_status)
```

## Count Updates

```python
counts = updates(
    vp,
    start_date="2026-06-24T18:20:00",
    end_date="2026-06-24T18:25:00",
    bmp_feed_type="bmp_adj_in_pre",
    return_count=True,
    base_url=BASE_URL,
    api_key=API_KEY,
)
print(counts["bmp"][str(vp.id)])
```

## Count RIB Entries

```python
route_count = rib(
    vp,
    date="2026-06-24T18:25:00",
    bmp_feed_type="bmp_adj_in_pre",
    return_count=True,
    base_url=BASE_URL,
    api_key=API_KEY,
)
print(route_count["bmp"][str(vp.id)])
```

## Build Topology

```python
graph = topology(
    vp,
    date="2026-06-24",
    bmp_feed_type="bmp_adj_in_pre",
    with_rib=True,
    base_url=BASE_URL,
    api_key=API_KEY,
)
print(len(graph["links"]))
```

## Count Messages

```python
bucketed = messages(
    vp,
    start_date="2026-06-24T18:20:00",
    end_date="2026-06-24T18:25:00",
    interval_time=60,
    base_url=BASE_URL,
    api_key=API_KEY,
)
print(bucketed[0])
```

## Monitoring

```python
session_counts = monitoring(
    start_date="2026-06-24T18:20:00",
    end_date="2026-06-24T18:25:00",
    bmp_parent_asns=[1000],
    frequency=300,
    base_url=BASE_URL,
    api_key=API_KEY,
)
print(session_counts.keys())
```

Live caveat: `production_testing` currently returns a server error for `/monitoring`; this call is valid for deployments where monitoring has a configured DB helper.
