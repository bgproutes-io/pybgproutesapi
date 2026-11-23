from unittest.mock import patch

from pybgproutesapi.endpoints.routers import parse_routers


def test_parse_routers_builds_vp_objects():
    payload = {
        "bgp": [{
            "name": "r1",
            "asn": 64500,
            "ip": "192.0.2.254",
            "country": "DE",
            "vantage_points": [{
                "id": 7,
                "ip": "192.0.2.1",
                "asn": 64501,
                "vrf_name": "default",
            }],
        }],
        "bmp": [],
    }
    parsed = parse_routers(payload)
    assert parsed["bgp"][0]["name"] == "r1"
    assert parsed["bgp"][0]["vantage_points"][0].unique_id == 7
    assert parsed["bgp"][0]["vantage_points"][0].peering_protocol == "bgp"


def test_routers_client_sends_filters():
    from pybgproutesapi.endpoints import routers as endpoint

    with patch.object(endpoint, "get", return_value={"bgp": [], "bmp": []}) as request:
        result = endpoint.routers(
            peering_protocol="bmp",
            bmp_parent_asns=[1000, 1001],
            base_url="https://example.test/v1",
            api_key="secret",
        )

    assert result == {"bgp": [], "bmp": []}
    assert request.call_args.args[0] == "/routers"
    assert request.call_args.args[1]["bmp_parent_asns"] == "1000,1001"
