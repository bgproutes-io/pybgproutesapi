from pybgproutesapi import messages, rib, topology, updates, vantage_points


BASE_URL = "http://192.168.130.1:8080"
API_KEY = "test"


def main():
    vp = vantage_points(vp_bmp_ids=[1], base_url=BASE_URL, api_key=API_KEY)[0]

    print("VP:", vp)
    print(
        "Updates:",
        updates(
            vp,
            "2026-06-24T18:20:00",
            "2026-06-24T18:25:00",
            bmp_feed_type="bmp_adj_in_pre",
            return_count=True,
            base_url=BASE_URL,
            api_key=API_KEY,
        )["bmp"][str(vp.id)],
    )
    print(
        "RIB count:",
        rib(
            vp,
            "2026-06-24T18:25:00",
            bmp_feed_type="bmp_adj_in_pre",
            return_count=True,
            base_url=BASE_URL,
            api_key=API_KEY,
        )["bmp"][str(vp.id)],
    )
    print(
        "Topology keys:",
        topology(
            vp,
            "2026-06-24",
            bmp_feed_type="bmp_adj_in_pre",
            base_url=BASE_URL,
            api_key=API_KEY,
        ).keys(),
    )
    print(
        "Message buckets:",
        len(
            messages(
                vp,
                "2026-06-24T18:20:00",
                "2026-06-24T18:25:00",
                interval_time=60,
                base_url=BASE_URL,
                api_key=API_KEY,
            )[0][2]
        ),
    )


if __name__ == "__main__":
    main()
