# hunt_log.py
"""Journal de chasse : chaque scan laisse sa trace."""
import json, os
from datetime import datetime, timezone

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hunt_log.json")

def log_scan(domain, n_keys, flags, scanner="roca", notes=""):
    entry = {
        "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "domain": domain,
        "scanner": scanner,
        "n_keys": n_keys,
        "flags": flags,
        "notes": notes,
    }
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            log = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        log = []
    log.append(entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    print(f"[hunt_log] trace ajoutee : {domain} ({n_keys} cles, {flags} drapeau(x))")
    return entry

if __name__ == "__main__":
    import sys
    d = sys.argv[1] if len(sys.argv) > 1 else "test"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    fl = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    log_scan(d, n, fl)
