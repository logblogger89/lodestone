"""Check which Lodestone sources this environment can reach.

Run: python3 scripts/check_network.py
Prints a reachable/blocked line per domain, and the domains to add if any are blocked.
"""
import pathlib
import urllib.error
import urllib.request

LIST = pathlib.Path(__file__).resolve().parent.parent / "config" / "network_allowlist.txt"


def probe(url: str) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": "Lodestone/0.1 (personal job search)"})
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
    if blocked:
        print("\nAdd these under Allowed domains (environment settings → Network access):")
        print("\n".join(f"  {d}" for d in blocked))
    else:
        print("\nAll sources reachable.")


if __name__ == "__main__":
    main()
