#!/usr/bin/env python3
"""roca_scanner.py - detect RSA moduli with the ROCA structural flaw.

CVE-2017-15361 (Infineon RSALib). A badly-born modulus has, for a list
of small marker primes p, the property that N mod p is a power of 2.
This scanner runs that fast screen without factoring anything.

Usage:
    python roca_scanner.py --selftest
    python roca_scanner.py <modulus_hex_or_dec> [...]
    python roca_scanner.py --file keys.txt
"""
import sys

PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
          53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
          109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167]

def _powers_of_two_mod(p):
    seen, x = set(), 1
    while x not in seen:
        seen.add(x)
        x = (x * 2) % p
    return seen

MARKS = {p: _powers_of_two_mod(p) for p in PRIMES}

def is_roca_suspect(n):
    return all((n % p) in MARKS[p] for p in PRIMES)

def parse(token):
    token = token.strip().lower()
    if token.startswith("0x"):
        return int(token, 16)
    if all(c in "0123456789abcdef" for c in token) and any(c in "abcdef" for c in token):
        return int(token, 16)
    return int(token)

def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    if argv[1] == "--selftest":
        bad = 2 ** 2048              # power of two: trips every marker
        good = (2 ** 2048) + 65537   # generic number: fails the screen
        for label, n in (("bad ", bad), ("good", good)):
            verdict = "ROCA-SUSPECT" if is_roca_suspect(n) else "clean"
            print(f"[{label}] {n.bit_length()} bits -> {verdict}")
        return 0
    if argv[1] == "--file":
        with open(argv[2], "r", encoding="utf-8") as fh:
            mods = [parse(l) for l in fh if l.strip() and not l.startswith("#")]
    else:
        mods = [parse(a) for a in argv[1:]]
    flagged = 0
    for i, n in enumerate(mods):
        if is_roca_suspect(n):
            flagged += 1
            print(f"[!] KEY #{i} ({n.bit_length()} bits): ROCA-SUSPECT - bad birth")
        else:
            print(f"[ok] KEY #{i} ({n.bit_length()} bits): passes the screen")
    print(f"-- {len(mods)} keys screened, {flagged} flagged --")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
