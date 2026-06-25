from pybgproutesapi import (
    bmp_rib_with_status,
    bmp_updates_for_analysis,
    route_propagation_path,
    vantage_points,
)


BASE_URL = "http://192.168.130.1:8080"
API_KEY = "test"


def main():
    vp = vantage_points(vp_bmp_ids=[1], base_url=BASE_URL, api_key=API_KEY)[0]

    rows = bmp_rib_with_status(
        vp,
        "2026-06-24T18:25:00",
        prefix_exact_match=["14.1.0.0/16"],
        base_url=BASE_URL,
        api_key=API_KEY,
    )
    print("BMP RIB with status:", rows[0])

    updates_by_rib = bmp_updates_for_analysis(
        vp,
        "2026-06-24T18:20:00",
        "2026-06-24T18:25:00",
        adj_rib_type="in",
        max_updates_to_return=5,
        base_url=BASE_URL,
        api_key=API_KEY,
    )
    print("BMP updates for analysis:", updates_by_rib.keys())

    graph = route_propagation_path(
        vp,
        prefix="1.0.0.0/24",
        timestamp=1782325500,
        aspath="1 2",
        base_url=BASE_URL,
        api_key=API_KEY,
    )
    print("Propagation graph:", len(graph["nodes"]), "nodes,", len(graph["edges"]), "edges")


if __name__ == "__main__":
    main()
