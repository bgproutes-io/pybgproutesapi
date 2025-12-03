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
            if isinstance(updates_list, list):
                for upd in updates_list:
                    lines.append(f"  Update: {upd}")
            else:
                lines.append(f"  Update count: A: {updates_list['A']} W: {updates_list['W']}")
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
                if isinstance(values, list) and len(values) == 3:
                    aspath, community, bmp_feed_id = values
                    lines.append(f"  Prefix: {prefix}")
                    lines.append(f"    AS Path: {aspath}")
                    lines.append(f"    Communities: {community}")
                else:  # Fallback if structure changes
                    lines.append(f"  Prefix: {prefix} → {values}")
    return "\n".join(lines)
