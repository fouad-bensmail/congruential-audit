#!/usr/bin/env python3
"""
cunningham_crible.py — case vide 3 de la table de Mendeleïev (Note X, §6)
Chaines de Cunningham de premiere espece, longueur L :
p, 2p+1, 4p+3, ..., 2^(L-1)p + 2^(L-1) - 1 tous premiers.
Constante C_L par produit d'Euler ; prediction affine dyadique
integrale de dt / prod ln(2^i t). Aucun parametre libre.
L=2 doit reproduire la Note X (§4.1) : 1.32032 / 7746 / 0.9917 a 10^6.
Pur Python 3, sans bibliotheque.

Usage : python cunningham_crible.py [X] [L_max]   (defaut : 1000000 4)
"""
import math, sys, time
import hunt_log

def crible_table(n):
    t = bytearray([1]) * (n + 1)
    t[0:2] = b"\x00\x00"
    for i in range(2, math.isqrt(n) + 1):
        if t[i]:
            t[i*i::i] = bytearray(len(t[i*i::i]))
    return t

def constante_L(L, premiers):
    S = 1.0
    for q in premiers:
        if q == 2:
            nu = 1
        else:
            nu = len({pow(2, i, q) for i in range(L)})
        S *= (1.0 - nu / q) * (1.0 - 1.0 / q) ** (-L)
    return S

def integrale_affine(X, L):
    def f(t):
        d = 1.0
        for i in range(L):
            d *= math.log(t * (1 << i))
        return 1.0 / d
    s = 0.0
    t = 2.0
    while t < X:
        b = min(t + 1.0, float(X))
        s += (b - t) * (f(t) + f(b)) / 2.0
        t = b
    return s

def compter_chaines(table, X, L):
    n = 0
    for p in range(2, X + 1):
        if not table[p]:
            continue
        v = p
        ok = True
        for _ in range(L - 1):
            v = 2 * v + 1
            if not table[v]:
                ok = False
                break
        if ok:
            n += 1
    return n

def main():
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    Lmax = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    t0 = time.time()
    haut = (1 << (Lmax - 1)) * (X + 1)
    table = crible_table(max(haut, 1_000_001))
    premiers = [i for i in range(2, 1_000_001) if table[i]]
    print(f"[*] Cunningham — X = {X}, L = 2..{Lmax}  ({time.time()-t0:.1f} s)")
    print(f" L |     C_L   |  mesure | prediction | ratio")
    notes = []
    for L in range(2, Lmax + 1):
        C = constante_L(L, premiers)
        pred = C * integrale_affine(X, L)
        n = compter_chaines(table, X, L)
        print(f"{L:>2} | {C:9.5f} | {n:7d} | {pred:10.1f} | {n/pred:.4f}")
        notes.append(f"L{L}={n}/{pred:.0f}")
    print("    (L=2 doit rendre 1.32032 / 7746 / 0.9917 : Note X §4.1)")
    hunt_log.log_scan("cunningham", X, 0, scanner="cunningham",
                      notes="; ".join(notes))

if __name__ == "__main__":
    main()
