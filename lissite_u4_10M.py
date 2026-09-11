#!/usr/bin/env python3
"""
lissite_u4_10M.py — Repesee du residu u=4 a X=10^7.

Double mesure a 10^7 :
  1) p-1 : P(P+(p-1) <= (p-1)^{1/u}) pour u=2,3,4,5 (reference) ;
  2) modele corrige : m pair, m+1 sans facteur <= Q (Q=sqrt(X)=3162).

Compare les ratios modele_corrige / mesure_p1 pour voir si le residu u=4
de l'Addendum X (0.9939 a 10^6) persiste (biais d'ordre deux) ou disparait
(fluctuation).

Usage : python -u lissite_u4_10M.py
"""
import math, time
from array import array

def crible_premiers(z):
    t = bytearray([1]) * (z + 1)
    t[0:2] = b"\x00\x00"
    for i in range(2, int(z ** 0.5) + 1):
        if t[i]:
            t[i*i:z+1:i] = bytearray(len(range(i*i, z+1, i)))
    return [p for p in range(2, z + 1) if t[p]]

def main():
    X = 10_000_000
    Q = int(X ** 0.5)
    t0 = time.time()

    # 1) crible lpf : plus grand facteur premier de chaque n <= X
    print(f"[1/4] crible lpf jusqu'a {X}...")
    lpf = array('I', [0]) * (X + 1)
    for i in range(2, X + 1):
        if lpf[i] == 0:
            for j in range(i, X + 1, i):
                lpf[j] = i

    # 2) crible des premiers jusqu'a X
    print(f"[2/4] crible des premiers jusqu'a {X}...")
    primes = crible_premiers(X)
    print(f" {len(primes)} premiers")

    # 3) mesure p-1
    print(f"[3/4] mesure p-1 a X={X}...")
    cnt_p1 = {2: 0, 3: 0, 4: 0, 5: 0}
    n_p1 = 0
    for p in primes:
        if p < 3:
            continue
        n_p1 += 1
        m = p - 1
        u = math.log(m) / math.log(lpf[m])
        for u0 in cnt_p1:
            if u >= u0:
                cnt_p1[u0] += 1

    prop_p1 = {u0: cnt_p1[u0] / n_p1 for u0 in cnt_p1}

    # 4) modele corrige : m pair, m+1 sans facteur <= Q
    print(f"[4/4] modele corrige (Q={Q})...")
    bad = bytearray(X + 1)
    for q in crible_premiers(Q):
        if q == 2:
            continue
        for m in range(q - 1, X + 1, q):
            bad[m] = 1

    cnt_mod = {2: 0, 3: 0, 4: 0, 5: 0}
    n_mod = 0
    for m in range(4, X + 1, 2):
        if bad[m]:
            continue
        n_mod += 1
        u = math.log(m) / math.log(lpf[m])
        for u0 in cnt_mod:
            if u >= u0:
                cnt_mod[u0] += 1

    prop_mod = {u0: cnt_mod[u0] / n_mod for u0 in cnt_mod}

    # 5) rapport
    print(f"\n[X] lissite_u4_10M — X={X}, n_p1={n_p1}, n_mod={n_mod}, Q={Q}")
    print(f" u | mesure p-1 | modele corrige | ratio | ecart vs 1.0")
    notes = []
    for u0 in (2, 3, 4, 5):
        r = prop_mod[u0] / prop_p1[u0]
        e = r - 1.0
        notes.append(f"u{u0}:{r:.4f}")
        print(f" {u0} | {prop_p1[u0]:.5f} | {prop_mod[u0]:.5f} "
              f"| {r:.4f} | {e:+.4f}")
    print(f"\n[OK] {time.time() - t0:.1f} s.")
    print(f"[NOTE] {' / '.join(notes)}")

if __name__ == "__main__":
    main()
