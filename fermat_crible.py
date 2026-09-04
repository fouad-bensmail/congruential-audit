#!/usr/bin/env python3
"""
fermat_crible.py — compagnon de la Note Universelle VII (+ addendum v4)
Factorisation de Fermat criblée : couche de parité (mod 4) puis résidus
quadratiques modulo 14 petits premiers. Outil DIAGNOSTIQUE de clés faibles
(facteurs proches), esprit FIPS 186. Pur Python 3, sans bibliothèque.

Usage :
  python fermat_crible.py --demo                 # table de reproduction (13 chiffres)
  python fermat_crible.py --n 1000000007000000021
  python fermat_crible.py --corpus moduli.txt    # diagnostic sur la moisson
"""
import argparse, time
from math import isqrt
import hunt_log

PREMIERS = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

# ---------------- utilités ----------------
def est_premier(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2; r += 1
    for a in (2, 3, 5, 7, 11, 13):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

def premier_apres(m):
    n = m if m % 2 else m + 1
    while not est_premier(n):
        n += 2
    return n

def ancre_parite(N, x):
    """Note VII §1 : N ≡ 1 (mod 4) ⇒ X impair ; N ≡ 3 (mod 4) ⇒ X pair."""
    if N % 4 == 1:
        return x if x % 2 else x + 1
    return x if x % 2 == 0 else x + 1

def tables_autorisees(N):
    """Pour chacun des 14 premiers : ok[r] = (r² − N est résidu quadratique mod p)."""
    tables = []
    for p in PREMIERS:
        qr = {(t * t) % p for t in range(p)}
        tables.append((p, [((r * r - N) % p) in qr for r in range(p)]))
    return tables

# ---------------- les deux Fermat ----------------
def fermat_naif(N, budget=10_000_000):
    x = isqrt(N)
    if x * x < N:
        x += 1
    for essais in range(1, budget + 1):
        t = x * x - N
        k = isqrt(t)
        if k * k == t:
            return x, k, essais
        x += 1
    return None

def fermat_crible(N, budget=2_000_000):
    x = ancre_parite(N, isqrt(N) + (1 if isqrt(N) ** 2 < N else 0))
    tables = tables_autorisees(N)
    vus = 0
    essais = 0
    while vus < budget:
        for p, ok in tables:
            if not ok[x % p]:
                break
        else:
            essais += 1
            t = x * x - N
            k = isqrt(t)
            if k * k == t:
                return x, k, essais
        x += 2
        vus += 2
    return None

# ---------------- lectures ----------------
def verdict(N, x, k, essais):
    p, q = x - k, x + k
    gap = q - p
    b = N.bit_length()
    seuil = isqrt(8 * isqrt(N))            # régime 2,83 · N^(1/4)
    print(f"    N = {N}")
    print(f"    facteurs : p={p}  q={q}")
    print(f"    ecart |q-p| = {gap}   (essais cribles : {essais})")
    if gap < seuil:
        print("    -> regime N^1/4 : cle FAIBLE (facteurs trop proches)")
    if b >= 256:
        print(f"    FIPS 186 : ecart minimal 2^{b-100} -> "
              + ("conforme" if gap > 2 ** (b - 100) else "NON conforme"))

def mode_demo():
    print("[*] Note VII — reproduction (semi-premiers de 13 chiffres)")
    p1 = premier_apres(3_162_000); q1 = premier_apres(p1 + 50)
    p2 = premier_apres(3_162_000); q2 = premier_apres(p2 + 5_000)
    p3 = premier_apres(2_000_000); q3 = premier_apres(5_000_000)
    print(f"{'cas':<20}| N mod 4 |  naif | crible")
    for nom, N in [("facteurs proches", p1*q1),
                   ("ecart modere    ", p2*q2),
                   ("ecart large     ", p3*q3)]:
        _, _, e_naif = fermat_naif(N)
        _, _, e_crible = fermat_crible(N)
        print(f"{nom:<20}|    {N % 4}    | {e_naif:>6} | {e_crible:>4}")

def mode_n(valeur, budget):
    N = int(valeur, 0)
    print(f"[*] Diagnostic Fermat crible ({N.bit_length()} bits), budget {budget}")
    res = fermat_crible(N, budget)
    if res is None:
        print("    aucun facteur proche dans la fenetre : rien a signaler")
        hunt_log.log_scan("fermat-N", 1, 0, scanner="fermat",
                          notes=f"bits={N.bit_length()}, budget={budget}")
    else:
        verdict(N, *res)
        hunt_log.log_scan("fermat-N", 1, 1, scanner="fermat",
                          notes=f"bits={N.bit_length()}")

def mode_corpus(fichier, budget):
    moduli = [int(l.strip(), 16) for l in open(fichier, encoding="utf-8") if l.strip()]
    faibles = 0
    t0 = time.time()
    for i, N in enumerate(moduli):
        res = fermat_crible(N, budget)
        if res is not None:
            faibles += 1
            print(f"    ! modulus #{i} : FACTEURS TROUVES")
            verdict(N, *res)
        if (i + 1) % 50 == 0:
            print(f"    ... {i+1}/{len(moduli)} modulus ({time.time()-t0:.0f} s)")
    print(f"[OK] Fermat crible : {len(moduli)} modulus, {faibles} faible(s).")
    hunt_log.log_scan("corpus-fermat", len(moduli), faibles, scanner="fermat",
                      notes=f"budget={budget}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--n")
    ap.add_argument("--corpus")
    ap.add_argument("--budget", type=int, default=20_000)
    args = ap.parse_args()
    if args.demo:
        mode_demo()
    elif args.n:
        mode_n(args.n, args.budget)
    elif args.corpus:
        mode_corpus(args.corpus, args.budget)
    else:
        print("[!] choisissez --demo, --n ou --corpus")

if __name__ == "__main__":
    main()
