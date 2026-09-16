#!/usr/bin/env python3
"""
sophie_germain.py — la lissite de p-1 pour les premiers de Sophie Germain.

Etend le cadre aux premiers de Sophie Germain (p premier et 2p+1 premier).
Ces premiers ont une contrainte congruentielle forte : p = 2 mod 3 (sauf p=3),
donc v_3(p-1) = 0. On mesure la lissite de p-1 et on la compare aux premiers
ordinaires dans la classe 2 mod 3.

Usage : python -u sophie_germain.py

Gardes annoncees :
  [0] Contrainte congruentielle : les premiers SG sont tous ≡ 2 mod 3, donc
      v_3(p-1) = 0. Garde : proportion de SG avec v_3(p-1) >= 1 est 0.
  [1] Lissite de p-1 pour les SG, comparee aux premiers ordinaires de la
      classe 2 mod 3. On s'attend a des proportions similaires (la contrainte
      principale est v_3 = 0) : le ratio SG/cls2 doit etre proche de 1.
  [2] Stabilite du ratio entre echelles 10^6 et 10^7.

Note : les premiers SG sont rares (densite ~ 1/(log X)^2). A u=5, les
effectifs sont maigres ; la lecture se fait surtout a u=2 et u=3.
"""
import math
import time
from array import array
import hunt_log

US = (2, 3, 4, 5)
SCALES = (10**6, 10**7)

def primes_to(n):
    c = bytearray([1]) * (n + 1)
    c[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if c[i]:
            c[i * i::i] = bytearray(len(range(i * i, n + 1, i)))
    return c

def gpf_sieve(n):
    """gpf[m] = P+(m) (plus grand facteur premier), par ecrasement ascendant."""
    gpf = array('I', [0]) * (n + 1)
    for p in range(2, n + 1):
        if gpf[p] == 0:
            gpf[p::p] = array('I', [p]) * len(range(p, n + 1, p))
    return gpf

def weigh_scale(X, sieve, gpf):
    # Premiers de Sophie Germain jusqu'a X
    sg = []
    for p in range(2, X + 1):
        if sieve[p] and sieve[2 * p + 1]:
            sg.append(p)
    # Premiers ordinaires dans la classe 2 mod 3 jusqu'a X
    cls2 = [p for p in range(5, X + 1) if sieve[p] and p % 3 == 2]

    def smooth_props(primes):
        counts = {u: 0 for u in US}
        v3_ge1 = 0
        for p in primes:
            m = p - 1
            if m % 3 == 0:
                v3_ge1 += 1
            for u in US:
                if gpf[m] <= m ** (1.0 / u):
                    counts[u] += 1
        n = len(primes)
        return {u: counts[u] / n for u in US}, n, v3_ge1

    sg_props, n_sg, sg_v3 = smooth_props(sg)
    c2_props, n_c2, _ = smooth_props(cls2)
    return sg_props, n_sg, sg_v3, c2_props, n_c2

def main():
    t0 = time.time()
    Xmax = max(SCALES)

    print("=" * 78)
    print("LISSITE DE p-1 POUR LES PREMIERS DE SOPHIE GERMAIN")
    print(f"echelles {SCALES}")
    print("=" * 78)

    print("\ngeneration du crible jusqu'a 2*10^7+1 ...")
    sieve = primes_to(2 * Xmax + 1)
    print("generation du crible gpf jusqu'a 10^7 ...")
    gpf = gpf_sieve(Xmax)

    R = {}
    for X in SCALES:
        print(f"\npesee X = {X} ...")
        R[X] = weigh_scale(X, sieve, gpf)

    # [0] garde congruentielle
    print("\n[0] garde congruentielle : v_3(p-1) = 0 pour les premiers SG")
    for X in SCALES:
        sg_props, n_sg, sg_v3, c2_props, n_c2 = R[X]
        prop_v3 = sg_v3 / n_sg if n_sg > 0 else 0
        print(f"      X={X} : {n_sg} premiers SG, proportion avec v_3(p-1)>=1 : {prop_v3:.6f}")

    # [1] lissite SG vs classe 2 mod 3
    print("\n[1] lissite de p-1 : SG vs premiers ordinaires classe 2 mod 3")
    print("      u   SG(10^6)    cls2(10^6)  SG(10^7)    cls2(10^7)  ratio SG/cls2")
    for u in US:
        sg6, c26 = R[SCALES[0]][0][u], R[SCALES[0]][3][u]
        sg7, c27 = R[SCALES[1]][0][u], R[SCALES[1]][3][u]
        r6 = sg6 / c26 if c26 > 0 else 0
        r7 = sg7 / c27 if c27 > 0 else 0
        print(f"      {u}   {sg6:<11.6f} {c26:<11.6f} {sg7:<11.6f} {c27:<11.6f} {r6:.4f} / {r7:.4f}")

    # [2] stabilite
    print("\n[2] stabilite du ratio SG/cls2 entre echelles")
    for u in US:
        sg6, c26 = R[SCALES[0]][0][u], R[SCALES[0]][3][u]
        sg7, c27 = R[SCALES[1]][0][u], R[SCALES[1]][3][u]
        r6 = sg6 / c26 if c26 > 0 else 0
        r7 = sg7 / c27 if c27 > 0 else 0
        if r6 > 0:
            print(f"      u={u} : ratio(10^6)={r6:.4f} -> ratio(10^7)={r7:.4f}")

    print("\n" + "=" * 78)
    print(f"[OK] {time.time()-t0:.1f} s")
    hunt_log.log_scan("sophie-germain", len(US), 0,
                      scanner="sophie_germain",
                      notes=f"n_sg(10^7)={R[SCALES[1]][1]}")

if __name__ == "__main__":
    main()