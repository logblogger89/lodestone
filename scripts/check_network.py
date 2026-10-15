"""Check which Lodestone sources this environment can reach.

Run: python3 scripts/check_network.py
Prints a reachable/blocked line per domain, and the domains to add if any are blocked.
"""
import concurrent.futures as cf
import pathlib
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIST = ROOT / "config" / "network_allowlist.txt"
sys.path.insert(0, str(ROOT))


def probe(url: str) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Lodestone personal job search)"})
    try:
        urllib.request.urlopen(req, timeout=15)
        return True
    except urllib.error.HTTPError:
        return True  # the server answered (e.g. 404 for a dummy slug), so the network path is open
    except Exception:
        return False


def main() -> None:
    blocked = []
    for line in LIST.read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        domain, url, purpose = line.split(None, 2)
        ok = probe(url)
        print(f"{'reachable' if ok else 'BLOCKED  '}  {domain:28} {purpose}")
        if not ok:
            blocked.append(domain)
    # Every careers-site host in the source index is checked too, so new sources need no extra step.
    from lodestone import sources
    hosts = sorted({h for r in sources.load() if r["status"] == "active" for h in [sources.row_host(r)] if h})
    with cf.ThreadPoolExecutor(16) as ex:
        results = list(ex.map(lambda h: (h, probe(f"https://{h}/")), hosts))
    bad = [h for h, ok in results if not ok]
    print(f"\nSource index: {len(hosts) - len(bad)} of {len(hosts)} careers-site hosts reachable.")
    for h in bad:
        print(f"BLOCKED    {h}")
    blocked += bad
    if blocked:
        print("\nAdd these under Allowed domains (environment settings → Network access):")
        print("\n".join(f"  {d}" for d in blocked))
    else:
        print("\nAll sources reachable.")


if __name__ == "__main__":
    main()
