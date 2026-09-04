#!/usr/bin/env python3
"""
mendeleev_vides.py — cases vides de la table de Mendeleïev (Note X, §6) — labo privé
Case 1 : seconde famille de triplets (p, p+4, p+6) : prédiction = même constante S3.
Case 2 : quadruplets (p, p+2, p+6, p+8) : constante S4 par produit d'Euler.
Aucun paramètre libre. Pur Python 3, sans bibliothèque.

Usage : python mendeleev_vides.py [X]   (défaut : 1000000)
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

def constante_hl(motif, premiers):
    """S = prod_q (1 - nu_q/q)(1 - 1/q)^(-k), nu_q = classes occupees par le motif mod q."""
    k = len(motif)
    S = 1.0
    for q in premiers:
        nu = len({m % q for m in motif})
        S *= (1.0 - nu / q) * (1.0 - 1.0 / q) ** (-k)
    return S

def integrale(X, k):
    s = 0.0
    t = 2.0
    while t < X:
        b = min(t + 1.0, float(X))
        s += (b - t) * (1.0/math.log(t)**k + 1.0/math.log(b)**k) / 2.0
        t = b
    return s

def main():
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    t0 = time.time()
    table = crible_table(max(X + 8, 1_000_001))
    premiers = [i for i in range(2, 1_000_001) if table[i]]

    S3  = constante_hl((0, 2, 6), premiers)
    S3b = constante_hl((0, 4, 6), premiers)
    S4  = constante_hl((0, 2, 6, 8), premiers)

    nA = nB = nQ = 0
    for p in range(3, X - 8):
        if table[p]:
            if table[p+2] and table[p+6]:
                nA += 1
            if table[p+4] and table[p+6]:
                nB += 1
            if table[p+2] and table[p+6] and table[p+8]:
                nQ += 1

    i3, i4 = integrale(X, 3), integrale(X, 4)
    pA, pB, pQ = S3*i3, S3b*i3, S4*i4
    print(f"[*] Cases vides de Mendeleïev — X = {X}  ({time.time()-t0:.1f} s)")
    print(f"    S3  (p,p+2,p+6) = {S3:.5f}")
    print(f"    S3' (p,p+4,p+6) = {S3b:.5f}   <- case vide 1 : meme constante")
    print(f"    S4  quadruplets = {S4:.5f}")
    print(f"    triplets A  : {nA:>6}  prediction {pA:>8.1f}  ratio {nA/pA:.4f}")
    print(f"    triplets B  : {nB:>6}  prediction {pB:>8.1f}  ratio {nB/pB:.4f}")
    print(f"    quadruplets : {nQ:>6}  prediction {pQ:>8.1f}  ratio {nQ/pQ:.4f}")
    hunt_log.log_scan("mendeleev-vides", X, 0, scanner="mendeleev",
                      notes=f"A={nA} B={nB} Q={nQ}")

if __name__ == "__main__":
    main()
