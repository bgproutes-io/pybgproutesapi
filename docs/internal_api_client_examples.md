# Internal API Client Examples

These examples require `IS_DEPLOYED_INTERNALLY=True` on the API server.

```python
from pybgproutesapi import (
    vantage_points,
    bmp_rib_with_status,
    bmp_updates_for_analysis,
    route_propagation_path,
)

BASE_URL = "http://192.168.130.1:8080"
API_KEY = "test"

vp = vantage_points(vp_bmp_ids=[1], base_url=BASE_URL, api_key=API_KEY)[0]
```

## BMP RIB With Status

```python
rows = bmp_rib_with_status(
    vp,
    date="2026-06-24T18:25:00",
    prefix_exact_match=["14.1.0.0/16"],
    base_url=BASE_URL,
    api_key=API_KEY,
)
print(rows[0])
```

Expected row shape:

```python
[
    "14.1.0.0/16",
    ["7 14", "7 14"],
    ["7:10", "1000:10"],
    [None, None],
    [None, None],
    ["179.0.77.7", "179.0.77.7"],
    [1, 1],
    [1782325175.352203, 1782325175.352203],
    ["I,I", "I,I"],
    "I",
    0,
    "accepted",
]
```

## BMP Updates For Analysis

```python
updates_by_rib = bmp_updates_for_analysis(
    vp,
    start_date="2026-06-24T18:20:00",
    end_date="2026-06-24T18:25:00",
    adj_rib_type="in",
    max_updates_to_return=5,
    base_url=BASE_URL,
    api_key=API_KEY,
)
print(updates_by_rib.keys())
```

## Route Propagation Path

```python
graph = route_propagation_path(
    vp,
    prefix="1.0.0.0/24",
    timestamp=1782325500,
    aspath="1 2",
    base_url=BASE_URL,
    api_key=API_KEY,
)
print(graph["nodes"])
print(graph["edges"])
```
