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
from pybgproutesapi import vantage_points, updates, rib

# Get vantage points in FR or US from RIS or PCH
vps = vantage_points(
    source=["ris", "pch"],
    country=["FR", "US"]
)
print (vps)

# Get updates from a VP during a 1-hour window
for update in updates(
    vp_ip="178.208.11.4",
    start_date="2025-05-09T10:00:00",
    end_date="2025-05-09T11:00:00",
    aspath_regexp=" 6830 "):
    
    print (update)

# Get RIB entries for a specific VP and for all prefixes contained in 8.0.0.0/8.
rib_data = rib(
    vp_ips=["187.16.217.110"],
    date='2025-05-09T20:00:00',
    return_community=False,
    prefix_filter=[('<<', '8.0.0.0/8')])

for prefix, (aspath, community) in rib_data["187.16.217.110"].items():
    print(prefix, aspath, community)
```

## 📘 API endpoints

This library wraps four main endpoints:

| Function          | API Endpoint       | Description                            |
|-------------------|--------------------|----------------------------------------|
| `vantage_points()`| `/vantage_points`  | List and filter vantage point metadata |
| `updates()`       | `/updates`         | Query BGP updates                      |
| `rib()`           | `/rib`             | Retrieve RIB entries at a given time   |
| `topology()`      | `/topology`        | Retrieve the AS-level topology         |

Each function supports the full range of query parameters and returns the `data` portion of the API response by default.  
If you want to access the full response (including duration and byte size), pass `resource_details=True`.

#### Example with resource details.

```python
result = vantage_points(
    source=["bgproutes.io"],
    country=["FR"],
    resource_details=True
)

print(result["seconds"], result["bytes"])
print(result["data"])
```

For detailed parameter descriptions, examples, and advanced usage, see the official [API documentation](https://bgproutes.io/data_api).

## Date Format

All date parameters must be provided in **ISO 8601** format and in **UTC**:

```
YYYY-MM-DDTHH:MM:SS
```

For example: `2025-05-10T12:10:05`

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

To help you manage your usage, the `vantage_points`, `updates`, and `rib` functions include a `resource_details` parameter.  
By default, it is set to `False`, returning only the requested data.  
If set to `True`, the response will also include metadata such as server execution time and the size of the downloaded response in bytes.  
This information can help you monitor your usage and optimize your queries to stay within your rate limits.

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

This will run the `test_examples.py` script, which executes all example files in the `examples/` directory to ensure they run without errors.

## Error Handling

If the API returns an error response (e.g. due to a bad query, invalid input, or exceeded rate limit), the client raises a corresponding Python exception.

You can catch these exceptions using:

```python
from pybgproutesapi.exceptions import InvalidQueryError, RateLimitExceededError, APIKeyError

try:
    updates(...)  # your query here
except InvalidQueryError as e:
    print("Query problem:", e)
except RateLimitExceededError as e:
    print("Rate limit hit:", e)
except APIKeyError as e:
    print("API key invalid or missing:", e)
except Exception as e:
    print("Other error:", e)
```

Available exceptions:
- `InvalidQueryError`: raised when your query has invalid parameters (e.g. bad prefix format, date, or IP)
- `RateLimitExceededError`: raised when you've reached your API key's rate limits
- `APIKeyError`: raised when your API key is missing or invalid
- Generic `Exception` for any unexpected server-side or network error

For detailed parameter descriptions, examples, and advanced usage, see the official [API documentation](https://bgproutes.io/data_api).

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
