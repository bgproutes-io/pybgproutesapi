from importlib import import_module
from types import SimpleNamespace

rib_endpoint = import_module("pybgproutesapi.endpoints.rib")


def test_rib_forwards_live_rov_option_and_defaults_false(monkeypatch):
    calls = []

    def fake_get(_path, params, _details, **_kwargs):
        calls.append(params)
        return params

    monkeypatch.setattr(rib_endpoint, "get", fake_get)
    vp = SimpleNamespace(peering_protocol="bgp", unique_id=1)

    rib_endpoint.rib(vp, "2026-10-07T00:00:00")
    rib_endpoint.rib(
        vp,
        "2026-10-07T00:00:00",
        get_live_rov_status=True,
    )

    assert calls[0]["get_live_rov_status"] is False
    assert calls[1]["get_live_rov_status"] is True
