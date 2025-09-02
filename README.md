# pybgproutesapi

**`pybgproutesapi`** is a lightweight Python client for the [bgproutes.io API](https://bgproutes.io/data_api).  
It provides convenient functions to query BGP vantage points, updates, and RIB snapshots directly from Python, without needing to manually build HTTP requests.

## Installation

<!-- ### Option 1: Install from PyPI (recommended)

```bash
pip install pybgproutesapi
```

### Option 2: Install from source -->

```bash
git clone https://github.com/bgproutes-io/pybgproutesapi.git
cd pybgproutesapi
pip install .
```

## 🚀 Quickstart

1. **Log in to [bgproutes.io](https://bgproutes.io) and [generate a new API key](https://bgproutes.io/apikey)** to query historical data.

2. **Set your API key**:

You can set the API key either via the shell **(recommended for security)**:

```bash
export BGP_API_KEY=your-api-key
```

Or directly in your Python code (useful for notebooks or quick scripts):

```python
import os
os.environ["BGP_API_KEY"] = "your-api-key"
```

3. **Use the library**:

```python
from pybgproutesapi import vantage_points, updates, rib, format_updates_response, format_rib_response, chunked, merge_responses
from datetime import datetime, timedelta

# Use current day minus one day
yesterday = datetime.utcnow() - timedelta(days=1)
start_time = yesterday.replace(hour=20, minute=0, second=0, microsecond=0)
end_time = yesterday.replace(hour=21, minute=0, second=0, microsecond=0)
rib_time = yesterday.replace(hour=22, minute=0, second=0, microsecond=0)

# Format in ISO 8601
start_date_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
end_date_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")
rib_date_str = rib_time.strftime("%Y-%m-%dT%H:%M:%S")

# Get vantage points in FR or US from RIS or PCH
vps = vantage_points(
    sources=["ris", "pch"],
    countries=["FR", "CH"],
    date=start_date_str,
    date_end=end_date_str
)

print (f'A total of {len(vps)} VPs have been found.')

# --- UPDATES: run by batches of 10 VPs ------------------------------------
updates_merged = {"bgp": {}, "bmp": {}}
for batch in chunked(vps, 10):
    resp = updates(
        batch,
        start_date=start_date_str,
        end_date=end_date_str,
        aspath_regexp=" 6830 "
    )
    updates_merged = merge_responses(updates_merged, resp)

print(format_updates_response(updates_merged))

# --- RIB: run by batches of 10 VPs ----------------------------------------
rib_merged = {"bgp": {}, "bmp": {}}
for batch in chunked(vps, 10):
    resp = rib(
        batch,
        date=rib_date_str,
        return_community=False,
        prefix_filter=[('<<', '8.0.0.0/8')]
    )
    rib_merged = merge_responses(rib_merged, resp)

print(format_rib_response(rib_merged))

```

## 📘 API endpoints

This library wraps four main endpoints:

| Function          | API Endpoint       | Description                            |
|-------------------|--------------------|----------------------------------------|
| `vantage_points()`| `/vantage_points`  | List and filter vantage point metadata |
| `updates()`       | `/updates`         | Query BGP updates                      |
| `rib()`           | `/rib`             | Retrieve RIB entries at a given time   |
| `topology()`      | `/topology`        | Retrieve the AS-level topology         |

Each function supports the full range of query parameters provided by the API and returns the `data` portion of the API response by default.  
For detailed parameter descriptions, usage examples, and advanced options, refer to the official [API documentation](https://bgproutes.io/data_api).

## List Format

A key difference between the REST API and this Python client is how list parameters are handled.  
> - In the API (via HTTP), list values must be provided as **comma-separated strings**.  
> - In the Python client, the same parameters should be passed as **Python lists**.

This applies specifically to the parameters `prefix_exact_match`, `aspath_exact_match`, and `prefix_filter`, `as_to_ignore`. If any of these are provided with an invalid type, a `TypeError` will be raised with a descriptive message.

## Date Format

All date parameters must be provided in **ISO 8601** format and in **UTC**:

```
YYYY-MM-DDTHH:MM:SS
```

For example: `2025-05-10T12:10:05`
There is only one exception for the `topology` (see documentation for further details).

# 🚦 Rate Limiting

Each API key is subject to usage limits to ensure fair access for all users:
- **Maximum requests per hour:** 1000
- **Maximum total server execution time per hour:** 5 minute
- **Maximum data volume downloaded per hour:** 100MB
- **Maximum number of concurrent query**: 1 (only one request can be processed at a time per API key)

Requests exceeding these limits will be rejected with status code `429 Too Many Requests`.

For the `rib` function, there are limits on the number of queried vantage points and prefixes to prevent excessive resource usage.  
In particular, retrieving full RIBs from all vantage points can consume significant bandwidth and server time.

To manage this, the following rules apply:
- If you query more than 10 prefixes, you are limited to a maximum of 10 vantage points.
- Conversely, if you query more than 10 vantage points, you are limited to a maximum of 10 exact-match prefixes.

To help you manage your usage, the `vantage_points`, `updates`, and `rib` functions include a `details` parameter.  
By default, it is set to `False`, returning only the requested data.  
If set to `True`, the response will also include metadata such as server execution time and the size of the downloaded response in bytes.  
This information can help you monitor your usage and optimize your queries to stay within your rate limits.

#### Example with details set to True.

```python
result = vantage_points(
    source=["bgproutes.io"],
    country=["FR"],
    details=True
)
```

result will be a dictionnary with four keys:
- `seconds`: the execution time of the request on our server
- `bytes`: the number of bytes transferred
- `info`: information about each VPs (`up`/`down`/`ignored`/`unknown`) for each peering protocol (`bgp` or `bmp`) 
- `data`: the data

With `details=False`, only the content of `data` would be returned.

## 🧪 Running Tests

To verify that the client and example scripts work as expected, you can run the included tests using `pytest`.

### 1. Install `pytest` (if not already installed)

```bash
pip install pytest
```

### 2. Run the test suite

From the root of the repository:

```bash
pytest -v
```

This will run the `test_examples.py` script, which executes example files in the `examples/` directory to ensure they run without errors.

## 📌 Advices

- Use `prefix_filter` and `aspath_regexp` to narrow down results efficiently
- Setting `return_count=True` can significantly improve performance when you just want totals

For more details, visit the full [bgproutes.io API Documentation](https://api.bgproutes.io).

## Contact

For bug reports or feature requests, feel free to open an issue or submit a pull request.

For all other inquiries, contact us at:

📧 `contact@bgproutes.io`


## 📝 License

GPLv3
