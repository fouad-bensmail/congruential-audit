#!/usr/bin/env python3
"""
paires_2d.py — la famille complete des paires de gap 2d
(jumeaux, cousins, sexy, et au-dela).
Pour chaque d, compte les paires (p, p+2d) avec p <= X et compare a
    pi_{2d}(X) ~ S(d) * Li2(X),
    S(d) = 1.32032... * prod_{p|d, p>=3} (p-1)/(p-2).
Zero parametre libre.

Usage : python paires_2d.py [X] [dmax]   (defaut : X = 10^8, d = 1..6)
"""
import sys, math, time
import hunt_log

def crible(haut):
    t = bytearray([1]) * (haut + 1)
    t[0:2] = b"\x00\x00"
    for i in range(2, int(haut ** 0.5) + 1):
        if t[i]:
            t[i*i:haut+1:i] = bytearray(len(range(i*i, haut+1, i)))
    return t

def li2(x):
    L = math.log(x)
    s, f = 0.0, 1.0
    for j in range(1, 8):
        s += f * x / L ** (j + 1)
        f *= j + 1
    return s

def constante_base():
    ps = crible(1_000_000)
    prod = 1.0
    for p in range(3, 1_000_000):
        if ps[p]:
            prod *= 1.0 - 1.0 / (p - 1) ** 2
    return 2.0 * prod

def facteur(d):
    f, dd, p = 1.0, d, 3
    while dd % 2 == 0:
        dd //= 2
    while p * p <= dd:
        if dd % p == 0:
            f *= (p - 1) / (p - 2)
            while dd % p == 0:
                dd //= p
        p += 2
    if dd > 1:
        f *= (dd - 1) / (dd - 2)
    return f

def main():
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000_000
    dmax = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    t0 = time.time()
    table = crible(X + 2 * dmax)
    premiers = [i for i in range(2, X + 1) if table[i]]
    base = constante_base()
    print(f"[*] Paires de gap 2d — X = {X}  ({time.time()-t0:.1f} s)")
    print(f"    constante de base 2*C2 = {base:.5f}")
    print(f" d | gap |   S(d)  |  mesure  | prediction | ratio")
    notes, rats = [], []
    for d in range(1, dmax + 1):
        g = 2 * d
        S = base * facteur(d)
        mesure = 0
        lim = X - g
        for p in premiers:
            if p > lim:
                break
            if table[p + g]:
                mesure += 1
        pred = S * li2(X)
        ratio = mesure / pred
        notes.append(f"d{d}:{ratio:.4f}")
        rats.append(ratio)
        print(f" {d:2d} | {g:3d} | {S:.5f} | {mesure:8d} | {pred:10.1f} | {ratio:.4f}")
    print(f"[OK] {dmax} familles : ratio min {min(rats):.4f} ; max {max(rats):.4f} ; ecart max {max(abs(r-1) for r in rats):.4f}  ({time.time()-t0:.1f} s)")
    hunt_log.log_scan("paires-2d", X, 0, scanner="paires_2d", notes=" ".join(notes))

if __name__ == "__main__":
    main()
