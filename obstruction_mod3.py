#!/usr/bin/env python3

# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# Non-commercial use only. Commercial use prohibited without written consent.
# =============================================================================
"""
obstruction_mod3.py — obstruction locale q=3 de la lissite de p-1,
conditionnee par p mod 3, avec la regle validee :
    P+(m) <= m^(1/u)
et non plus P+(m) <= X^(1/u).

Gardes :
  [0] etalon global : a 10^7, u=2 doit retrouver ~0.35583 ;
  [1] v3(p-1) moyen : classe 1 -> 1.5, classe 2 -> 0 ;
  [2] signature rho1 > rho2, 4/4 aux deux echelles ;
  [3] modele aveugle global/classe : <1 en classe 1, >1 en classe 2,
      persistant aux deux echelles.
Usage :
    python -u obstruction_mod3.py
"""
import math, time
from array import array
import hunt_log

US = (2, 3, 4, 5)
SCALES = (1_000_000, 10_000_000)

def primes_to(n):
    c = bytearray([1]) * (n + 1)
    c[0:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if c[i]:
            c[i*i:n+1:i] = bytearray(len(range(i*i, n+1, i)))
    return [i for i in range(2, n + 1) if c[i]]

def lpf_sieve(X):
    """
    lp[n] = plus grand facteur premier de n.
    La boucle monte les premiers ; chaque multiple est reecrit par le dernier
    premier qui le divise, donc le plus grand.
    """
    lp = array('I', [0]) * (X + 1)
    for p in range(2, X + 1):
        if lp[p] == 0:  # p premier
            lp[p::p] = array('I', [p]) * len(range(p, X + 1, p))
    return lp

def new_bucket():
    return {'n': 0, 's': {u: 0 for u in US}}

def prop(b, u):
    return b['s'][u] / b['n']

def weigh_scale(X):
    ps = primes_to(X)
    lp = lpf_sieve(X)

    g = new_bucket()
    cls = {1: new_bucket(), 2: new_bucket()}
    v3s = {1: 0, 2: 0}

    for p in ps:
        if p < 5:
            continue

        a = p % 3
        m = p - 1

        # valuation v3(p-1)
        t = m
        v = 0
        while t % 3 == 0:
            v += 1
            t //= 3
        v3s[a] += v

        # alimentation globale et classe
        for b in (g, cls[a]):
            b['n'] += 1
            for u in US:
                if lp[m] <= m ** (1.0 / u):
                    b['s'][u] += 1

    return dict(g=g, cls=cls, v3=v3s)

def main():
    t0 = time.time()
    R = {X: weigh_scale(X) for X in SCALES}
    r6 = R[1_000_000]
    r7 = R[10_000_000]

    print("[0/4] etalon global P+(p-1) <= (p-1)^(1/u) ...")
    for u in US:
        print(f"      u={u} : globale 10^7 = {prop(r7['g'], u):.5f}")
    anchor = abs(prop(r7['g'], 2) - 0.35583) < 1e-4
    print(f"      garde u=2 contre 0.35583 : {'OK' if anchor else 'ECHEC'}")

    print("[1/4] garde interne v3(p-1) ...")
    m1 = r7["v3"][1] / r7["cls"][1]["n"]
    m2 = r7["v3"][2] / r7["cls"][2]["n"]
    print(f"      v3 moyen classe 1 = {m1:.4f} (attendu 1,5) ; "
          f"classe 2 = {m2:.4f} (attendu 0)")
    g_v3 = abs(m1 - 1.5) < 0.02 and m2 == 0.0

    print("[2/4] signature rho1 - rho2 ...")
    sig6 = sig7 = 0
    gaps6 = []
    gaps7 = []

    for u in US:
        d6 = prop(r6["cls"][1], u) - prop(r6["cls"][2], u)
        d7 = prop(r7["cls"][1], u) - prop(r7["cls"][2], u)
        gaps6.append(d6)
        gaps7.append(d7)
        sig6 += d6 > 0
        sig7 += d7 > 0
        print(f"      u={u} : ecart 10^6 = {d6:+.5f} , ecart 10^7 = {d7:+.5f}")

    print(f"      signature 4/4 : 10^6 {sig6}/4 , 10^7 {sig7}/4")

    print("[3/4] modele aveugle global/classe : direction et persistence ...")
    ok_bl = True
    for u in US:
        b6_1 = prop(r6["g"], u) / prop(r6["cls"][1], u)
        b6_2 = prop(r6["g"], u) / prop(r6["cls"][2], u)
        b7_1 = prop(r7["g"], u) / prop(r7["cls"][1], u)
        b7_2 = prop(r7["g"], u) / prop(r7["cls"][2], u)

        ok_bl &= b6_1 < 1 < b6_2 and b7_1 < 1 < b7_2

        print(f"      u={u} : 10^6 aveugle1 {b6_1:.4f} aveugle2 {b6_2:.4f} | "
              f"10^7 aveugle1 {b7_1:.4f} aveugle2 {b7_2:.4f}")

    contr = gaps6[0] / gaps7[0] if gaps7[0] > 0 else 9.9
    print(f"      ecart rho1-rho2 (u=2) : 10^6 {gaps6[0]:+.5f} -> "
          f"10^7 {gaps7[0]:+.5f} (contraction x{contr:.2f})")

    ok = anchor and g_v3 and sig6 == 4 and sig7 == 4 and ok_bl and contr >= 1.05

    print(f"[verdict] obstruction mod 3 : {'VERT' if ok else 'REFUSE'}")
    print(f"[OK] {time.time() - t0:.1f} s")

    hunt_log.log_scan("obstruction-mod3-mrule", 4 if ok else 0, 0 if ok else 1,
                      scanner="obstruction_mod3",
                      notes=f"m-rule anchor:{anchor} v3:{m1:.3f}/{m2:.1f} "
                            f"sig:{sig6}/{sig7} contr:{contr:.2f}")

if __name__ == "__main__":
    main()