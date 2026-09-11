#!/usr/bin/env python3
"""
lissite_corrigee.py — Addendum X : le modele nul corrige de la lissite de p-1.

Modele nul corrige : m pair, m+1 sans aucun facteur premier <= Q (Q >= X^{1/2}).
Cette contrainte impose exactement les densites locales P(q | m) = 1/(q-1) du
biais de Dirichlet, en plus du biais de parite (m pair, partie impaire moitie).
On pese P(P+(m) <= m^{1/u}) pour u = 2, 3, 4, et on compare :
  - a Dickman naif rho(u) (rejete aux ratios 1.20 / 1.74 / 4.04) ;
  - a la MESURE publiee sur p-1 (Addendum VIII, freres_unis.txt, X=10^6).
Si le modele corrige colle a la mesure (ratios ~ 1.00), le biais a un corps.

Usage : python -u lissite_corrigee.py [X] [Q] (defaut X=10^6, Q=1000)
"""
import sys, math, time
from array import array
import hunt_log

# Mesure publiee (Addendum VIII / freres_unis.txt, X=10^6, 78 496 premiers)
MESURE = {2: 0.36817, 3: 0.08464, 4: 0.02009}
RHO = {2: 0.30685, 3: 0.04861, 4: 0.00497}

def crible_premiers(z):
    t = bytearray([1]) * (z + 1)
    t[0:2] = b"\x00\x00"
    for i in range(2, int(z ** 0.5) + 1):
        if t[i]:
            t[i*i:z+1:i] = bytearray(len(range(i*i, z+1, i)))
    return [p for p in range(2, z + 1) if t[p]]

def main():
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    Q = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    t0 = time.time()

    # 1) plus grand facteur premier de chaque m <= X
    lpf = array('I', [0]) * (X + 1)
    for i in range(2, X + 1):
        if lpf[i] == 0:
            for j in range(i, X + 1, i):
                lpf[j] = i

    # 2) interdits : m tel que m+1 ait un facteur premier <= Q
    # (m pair => m+1 impair : la condition en q=2 est vide)
    bad = bytearray(X + 1)
    for q in crible_premiers(Q):
        if q == 2:
            continue
        for m in range(q - 1, X + 1, q):
            bad[m] = 1

    # 3) pesee sur les m pairs survivants
    cnt = {2: 0, 3: 0, 4: 0}
    n = 0
    for m in range(4, X + 1, 2):
        if bad[m]:
            continue
        n += 1
        u = math.log(m) / math.log(lpf[m])
        for u0 in cnt:
            if u >= u0:
                cnt[u0] += 1

    print(f"[X] lissite corrigee — m pair, m+1 sans facteur <= {Q}, "
          f"X={X}, n={n}")
    print(" u | rho naive | mesure p-1 | modele corrige | corr/mesure | naive/mesure")
    notes = []
    for u0 in (2, 3, 4):
        mod = cnt[u0] / n
        rc = mod / MESURE[u0]
        rn = RHO[u0] / MESURE[u0]
        notes.append(f"u{u0}:{rc:.4f}")
        print(f" {u0} | {RHO[u0]:.5f} | {MESURE[u0]:.5f} | {mod:.5f} "
              f"| {rc:.4f} | {rn:.4f}")
    print(f"[OK] {time.time() - t0:.1f} s.")
    hunt_log.log_scan("lissite-corrigee", X, 0,
                      scanner="lissite_corrigee", notes=" ".join(notes))

if __name__ == "__main__":
    main()
