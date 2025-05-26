from datetime import datetime, timedelta
from pybgproutesapi import vantage_points, topology

# Use current day minus one day
yesterday = datetime.utcnow() - timedelta(days=1)
date = yesterday.replace(hour=20, minute=0, second=0, microsecond=0)
date_str = date.strftime("%Y-%m-%d")

i = 0

for source in ['routeviews', 'ris', 'pch']:
    # Store unique AS links (as tuples)
    all_links = set()

    outfile = f'links_{source}.txt'
    fd = open(outfile, 'w', 1)

    # Get all vantage points in a french network.
    vps = vantage_points(source=[source])[:100]

    print(f"{source}: Total vantage points: {len(vps)}")

    # Process in batches of 100
    batch_size = 100
    for i in range(0, len(vps), batch_size):
        batch = vps[i:i + batch_size]
        print(f"Processing batch {i // batch_size + 1} with {len(batch)} VPs...")
        
        try:
            topo = topology(batch, date_str)
            # Normalize links as tuples of integers
            for as1, as2 in topo["links"]:
                if as1 < as2:
                    all_links.add((as1, as2))
                else:
                    all_links.add((as2, as1))
        except Exception as e:
            print(f"Error processing batch {i // batch_size + 1}: {e}")
    
        i += 1

    for as1, as2 in all_links:
        fd.write(f'{as1} {as2}\n')

    fd.close()

    # Return total count of distinct links
    print(f"Total distinct AS links: {len(all_links)}")


def read_links(filename):
    with open(filename, 'r') as f:
        return set(tuple(map(int, line.strip().split())) for line in f if line.strip())

# Load link sets
pch_links = read_links('links_pch.txt')
ris_links = read_links('links_ris.txt')
rv_links = read_links('links_routeviews.txt')

# Intersections
all_three = pch_links & ris_links & rv_links

pch_ris_only = (pch_links & ris_links) - all_three
pch_rv_only = (pch_links & rv_links) - all_three
ris_rv_only = (ris_links & rv_links) - all_three

# Unique to one
only_pch = pch_links - (ris_links | rv_links)
only_ris = ris_links - (pch_links | rv_links)
only_rv = rv_links - (pch_links | ris_links)

# Output
print(f"Links in all three: {len(all_three)}")
print(f"Links only in PCH & RIS: {len(pch_ris_only)}")
print(f"Links only in PCH & RouteViews: {len(pch_rv_only)}")
print(f"Links only in RIS & RouteViews: {len(ris_rv_only)}")
print(f"Links only in PCH: {len(only_pch)}")
print(f"Links only in RIS: {len(only_ris)}")
print(f"Links only in RouteViews: {len(only_rv)}")

