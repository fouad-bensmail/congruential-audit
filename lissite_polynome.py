#!/usr/bin/env python3
"""
lissite_polynome.py — la lissite des valeurs polynomiales (Bunyakovsky).

Etend le cadre aux valeurs d'un polynome : pour P(n) = n^2 + 1, pese la
proportion de n <= X tels que P+(n^2+1) <= (n^2+1)^(1/u), pour u = 2..5.

Lecture structurelle : n^2 + 1 n'est divisible que par 2 et les premiers
≡ 1 mod 4 (theoreme : -1 est residu quadratique mod p ssi p = 2 ou p ≡ 1 mod 4).
Cette contrainte locale doit ecarter la proportion du modele de Dickman pour
entiers aleatoires, exactement comme le manuscrit (Observation 1) a rejete
Dickman pour p-1.

Usage : python -u lissite_polynome.py

Gardes annoncees :
  [0] Structure : P+(n^2+1) ≡ 1 mod 4 ou = 2 pour tout n (theoreme verifie).
      Garde : aucun ecart.
  [1] Proportions u-lisses et ratio au modele de Dickman rho(u). On s'attend
      a un ecart significatif (contrainte locale), sans valeur precise annoncee
      (premiere mesure).
  [2] Stabilite entre echelles 10^4 et 10^5 (queue de fluctuation ~1/sqrt(N)).
"""
import math
import time
import hunt_log

US = (2, 3, 4, 5)
SCALES = (10**4, 10**5)

# Fonction de Dickman rho(u) : proportion d'entiers aleatoires u-lisses.
RHO = {2: 0.3068528, 3: 0.0486084, 4: 0.0049104, 5: 0.0003543}

def primes_1mod4_to(n):
    """Retourne [2] + les premiers ≡ 1 mod 4 jusqu'a n."""
    c = bytearray([1]) * (n + 1)
    c[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if c[i]:
            c[i * i::i] = bytearray(len(range(i * i, n + 1, i)))
    return [2] + [p for p in range(5, n + 1) if c[p] and p % 4 == 1]

def largest_prime_factor(m, primes):
    """Plus grand facteur premier de m (m = n^2+1, facteurs ≡ 1 mod 4 ou 2)."""
    largest = 1
    for p in primes:
        if p * p > m:
            break
        if m % p == 0:
            largest = p
            while m % p == 0:
                m //= p
    if m > 1:
        largest = m
    return largest

def weigh_scale(X, primes):
    counts = {u: 0 for u in US}
    bad = 0
    for n in range(1, X + 1):
        m = n * n + 1
        P = largest_prime_factor(m, primes)
        if P > 2 and P % 4 != 1:
            bad += 1
        for u in US:
            if P <= m ** (1.0 / u):
                counts[u] += 1
    return {u: counts[u] / X for u in US}, bad

def main():
    t0 = time.time()
    Xmax = max(SCALES)
    primes = primes_1mod4_to(Xmax + 1)

    print("=" * 78)
    print("LISSITE DES VALEURS POLYNOMIALES — P(n) = n^2 + 1")
    print(f"echelles {SCALES}, {len(primes)} premiers autorises (2 et p ≡ 1 mod 4)")
    print("=" * 78)

    R = {}
    bad_total = 0
    for X in SCALES:
        print(f"\npesee X = {X} ...")
        props, bad = weigh_scale(X, primes)
        R[X] = props
        bad_total += bad

    print(f"\n[0] garde structure : P+(n^2+1) ≡ 1 mod 4 ou = 2")
    if bad_total == 0:
        print(f"      VERT : aucun facteur premier ≡ 3 mod 4 sur {sum(SCALES)} valeurs")
    else:
        print(f"      REFUS : {bad_total} valeurs avec facteur ≡ 3 mod 4")

    print("\n[1] proportions u-lisses contre modele de Dickman")
    print("      u   rho(Dickman)   mes(10^4)    mes(10^5)    ratio(10^5/rho)")
    for u in US:
        rho = RHO[u]
        m4 = R[SCALES[0]][u]
        m5 = R[SCALES[1]][u]
        ratio = m5 / rho if rho > 0 else 0
        print(f"      {u}   {rho:<12.6f}   {m4:<11.6f}   {m5:<11.6f}   {ratio:.4f}")

    print("\n[2] stabilite entre echelles")
    for u in US:
        m4 = R[SCALES[0]][u]
        m5 = R[SCALES[1]][u]
        if m4 > 0:
            print(f"      u={u} : mes(10^5)/mes(10^4) = {m5/m4:.4f}")

    verdict = ("AUDIT VERT : structure tenue, proportions mesurees"
               if bad_total == 0 else f"REFUS structure : {bad_total} ecarts")
    print("\n" + "=" * 78)
    print(f"VERDICT : {verdict}")
    print("=" * 78)
    print(f"[OK] {time.time()-t0:.1f} s")

    hunt_log.log_scan("lissite-polynome", len(US), bad_total,
                      scanner="lissite_polynome",
                      notes=f"n2+1 u2 mes(10^5)={R[SCALES[1]][2]:.6f} rho2={RHO[2]} bad={bad_total}")

if __name__ == "__main__":
    main()