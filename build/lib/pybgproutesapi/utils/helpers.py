# --- helpers ---------------------------------------------------------------
def chunked(seq, n):
    """Yield successive n-sized chunks from seq."""
    for i in range(0, len(seq), n):
        yield seq[i:i+n]

def merge_responses(dest, src):
    """Shallow-merge the standard response structure { 'bgp': {...}, 'bmp': {...} }."""
    if not src:
        return dest
    for proto in src.keys():  # typically 'bgp' and/or 'bmp'
        if proto not in dest or dest[proto] is None:
            dest[proto] = {}
        # src[proto] is a dict keyed by vp_id -> entries
        # a simple update is sufficient because vp_ids are disjoint across batches
        dest[proto].update(src[proto])
    return dest
# ---------------------------------------------------------------------------