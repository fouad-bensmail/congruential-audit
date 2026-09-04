#!/usr/bin/env python3
"""
sato_tate.py — compagnon de la Note Universelle IX (+ extension privée)
Traces de Frobenius, moments 1/2/4/6, masse en t=0, assert de Hasse.
E1: y2 = x3 - x + 1 (sans CM, disc -23)
E2: y2 = x3 - x     (CM par Z[i])
E3: y2 = x3 + 1     (CM par Z[w]) — extension privée
Pur Python 3, sans bibliothèque.

Usage : python sato_tate.py [X]   (défaut : 10000)
"""
import math, sys
import hunt_log

def premiers_jusqua(n):
    crible = bytearray([1]) * (n + 1)
    crible[0:2] = b"\x00\x00"
    for i in range(2, math.isqrt(n) + 1):
        if crible[i]:
            crible[i*i::i] = bytearray(len(crible[i*i::i]))
    return [i for i in range(2, n + 1) if crible[i]]

def table_qr(p):
    qr = bytearray(p)
    for r in range(p):
        qr[(r * r) % p] = 1
    return qr

def trace_frobenius(p, a, b, qr):
    s = 0
    for x in range(p):
        v = (x * x * x + a * x + b) % p
        if v == 0:
            continue
        s += 1 if qr[v] else -1
    return -s

def moments(a, b, mauvais, premiers):
    ts = []
    for p in premiers:
        if p in mauvais:
            continue
        qr = table_qr(p)
        ap = trace_frobenius(p, a, b, qr)
        assert ap * ap <= 4 * p, "Hasse violee !"
        t = ap / (2 * math.sqrt(p))
        ts.append(t)
    n = len(ts)
    return (n, sum(ts)/n, sum(t*t for t in ts)/n,
            sum(t**4 for t in ts)/n, sum(t**6 for t in ts)/n,
            sum(1 for t in ts if t == 0)/n)

def main():
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    premiers = premiers_jusqua(X)
    courbes = [
        ("E1 sans CM (y2=x3-x+1)", -1, 1, {2, 23}),
        ("E2 CM Z[i] (y2=x3-x)  ", -1, 0, {2}),
        ("E3 CM Z[w] (y2=x3+1)  ",  0, 1, {2, 3}),
    ]
    print(f"[*] Sato-Tate — {len(premiers)} premiers p <= {X}")
    print(f"{'courbe':<26}| n    | E[t] | E[t2] | E[t4] | E[t6] | frac(t=0)")
    for nom, a, b, mauvais in courbes:
        n, m1, m2, m4, m6, z = moments(a, b, mauvais, premiers)
        print(f"{nom:<26}|{n:>5}|{m1:>6.3f}|{m2:>6.3f}|{m4:>6.3f}|{m6:>6.3f}|{z:>6.3f}")
    print("    theorie ST : E[t2]=0.250 E[t4]=0.125 E[t6]=0.078 frac0=0.000")
    print("    theorie CM : E[t2]=0.250 E[t4]=0.188 E[t6]=0.156 frac0=0.500")
    hunt_log.log_scan("sato-tate", len(premiers), 0, scanner="sato_tate",
                      notes=f"X={X}")

if __name__ == "__main__":
    main()