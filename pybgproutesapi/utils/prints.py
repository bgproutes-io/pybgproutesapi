import json

def format_updates_response(response, as_json: bool = False) -> str:
    """
    Format updates response.
    If as_json=True → pretty JSON string.
    If as_json=False → human-readable text.
    """
    if as_json:
        return json.dumps(response, indent=2, ensure_ascii=False)
    
    lines = []
    for proto, vps in response.items():
        for vp_id, updates_list in vps.items():
            lines.append(f"Protocol: {proto} | Vantage Point: {vp_id}")
            if isinstance(updates_list, dict):  # BMP → feed types
                for feed_type, updates in updates_list.items():
                    lines.append(f"  Feed: {feed_type}")
                    for upd in updates:
                        lines.append(f"    Update: {upd}")
            else:  # BGP
                for upd in updates_list:
                    lines.append(f"  Update: {upd}")
    return "\n".join(lines)


def format_rib_response(response, as_json: bool = False) -> str:
    """
    Format RIB response.
    If as_json=True → pretty JSON string.
    If as_json=False → human-readable text.
    """
    if as_json:
        return json.dumps(response, indent=2, ensure_ascii=False)

    lines = []
    for proto, vps in response.items():
        for vp_id, entries in vps.items():
            lines.append(f"Protocol: {proto} | Vantage Point: {vp_id}")
            for prefix, values in entries.items():
                if isinstance(values, tuple) and len(values) == 2:
                    aspath, community = values
                    lines.append(f"  Prefix: {prefix}")
                    lines.append(f"    AS Path: {aspath}")
                    lines.append(f"    Communities: {community}")
                else:  # Fallback if structure changes
                    lines.append(f"  Prefix: {prefix} → {values}")
    return "\n".join(lines)
