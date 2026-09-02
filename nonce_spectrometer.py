#!/usr/bin/env python3
"""nonce_spectrometer.py - congruential bias detector for ECDSA nonces.

Weak nonce generators leave a fingerprint: the nonces are not uniform
modulo small primes. This tool screens a stream of nonces (one per
line, hex or decimal) with a chi-square test per marker prime.

Heuristic screen, not a lattice attack: it flags bias, it does not
recover keys.

Usage:
    python nonce_spectrometer.py --selftest
    python nonce_spectrometer.py --file nonces.txt
"""
import sys, secrets

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

def chi_square(counts, total, p):
    e = total / p
    return sum((c - e) ** 2 for c in counts) / e

def screen(nonces):
    if len(nonces) < 1000:
        print("warn: give me at least 1000 nonces for a stable screen")
    flagged = []
    for p in PRIMES:
        counts = [0] * p
        for k in nonces:
            counts[k % p] += 1
        stat = chi_square(counts, len(nonces), p)
        if stat > 10 * p:
            flagged.append((p, stat))
    return flagged

def parse(line):
    line = line.strip().lower()
    if not line or line.startswith("#"):
        return None
    return int(line, 16) if line.startswith("0x") or any(c in line for c in "abcdef") else int(line)

def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        clean = [secrets.randbelow(2**256) for _ in range(20000)]
        biased = [6 * secrets.randbelow(2**254) for _ in range(20000)]
        for label, stream in (("clean ", clean), ("biased", biased)):
            hits = screen(stream)
            if hits:
                detail = ", ".join(f"p={p}: x2={s:.0f}" for p, s in hits[:4])
                print(f"[{label}] BIASED  ({detail})")
            else:
                print(f"[{label}] uniform modulo the marker primes")
        return 0
    if len(argv) >= 3 and argv[1] == "--file":
        with open(argv[2], "r", encoding="utf-8") as fh:
            nonces = [v for v in (parse(l) for l in fh) if v is not None]
        hits = screen(nonces)
        if hits:
            print(f"[!] {len(nonces)} nonces: CONGRUENTIAL BIAS on " +
                  ", ".join(f"p={p}" for p, _ in hits))
        else:
            print(f"[ok] {len(nonces)} nonces: no congruential bias detected")
        return 0
    print(__doc__)
    return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv))
