#!/usr/bin/env python3
"""
crt_exact.py — Chapitre 1 du cadre : le CRT pesé exact.
Motif {n, n+2} : classes interdites nu_2 = 1, nu_p = 2 (p >= 3).
(a) periode pleine [1, P] : le compte des survivants doit etre EXACTEMENT |A| ;
(b) a X = 10^6 : ratio contre la densite exacte, borne |A|/X ;
(c) equidistribution : chaque classe survivante mod P recoit X/P + O(1).
Usage : python crt_exact.py [X] [z] (defaut X=10^6, z=7)
"""
import sys
from collections import Counter

def premiers(z):
    c = bytearray([1]) * (z + 1)
    c[0:2] = b"\x00\x00"
    for i in range(2, int(z ** 0.5) + 1):
        if c[i]:
            c[i*i:z+1:i] = bytearray(len(range(i*i, z+1, i)))
    return [p for p in range(2, z + 1) if c[p]]

def marquer(haut, S):
    surv = bytearray([1]) * (haut + 1)
    for p in S:
        classes = [0] if p == 2 else [0, (-2) % p]
        for r in classes:
            surv[r:haut+1:p] = bytearray(len(range(r, haut+1, p)))
    return surv

def main():
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    z = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    S = premiers(z)
    P = A = 1
    dens = 1.0
    for p in S:
        nu = 1 if p == 2 else 2
        P *= p; A *= (p - nu); dens *= (1 - nu / p)
    print(f"[CRT] S = premiers <= {z} : P = {P}, |A| = {A}, densite = {dens:.8f}")
    mesP = sum(marquer(P, S))
    print(f" (a) periode pleine : mesure {mesP} vs |A| = {A} -> "
          f"{'EXACT' if mesP == A else 'ECART'}")
    survX = marquer(X, S)
    mesX = sum(survX)
    pred = X * dens
    print(f" (b) X = {X} : mesure {mesX} vs prediction {pred:.1f} : "
          f"ratio {mesX / pred:.6f} (borne |A|/X = {A / X:.2e})")
    cnt = Counter(n % P for n in range(1, X + 1) if survX[n])
    vals = sorted(cnt.values())
    print(f" (c) equidistribution : {len(cnt)} classes occupees, "
          f"comptes min {vals[0]} max {vals[-1]} (ecart <= 1 attendu)")

if __name__ == "__main__":
    main()