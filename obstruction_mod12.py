#!/usr/bin/env python3

# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# Non-commercial use only. Commercial use prohibited without written consent.
# =============================================================================
"""
obstruction_mod12.py — obstruction conjointe q=2 et q=3,
conditionnement par p mod 12, avec la regle validee :
    P+(m) <= m^(1/u)
et non plus P+(m) <= X^(1/u).

Gardes :
  [0] etalon global : a 10^7, u=2 doit retrouver ~0.35583 ;
  [1] valuations moyennes (v2, v3) par classe mod 12 :
        c1  : (3.0, 1.5)
        c5  : (3.0, 0.0)
        c7  : (1.0, 1.5)
        c11 : (1.0, 0.0)
  [2] signature : c1 au-dessus, c11 au-dessous ;
  [3] multiplicativite authentique :
        D12(a) ≈ D4(a mod 4) * D3(a mod 3)
      dans 3 sigma ;
  [4] aveugle global/classe : <1 pour c1, >1 pour c11, persistant.
Usage :
    python -u obstruction_mod12.py
"""
import math, time
from array import array
import hunt_log

US = (2, 3, 4, 5)
SCALES = (1_000_000, 10_000_000)
CL12 = (1, 5, 7, 11)
ORDER = (1, 7, 5, 11)

EXP_V = {
    1:  (3.0, 1.5),
    5:  (3.0, 0.0),
    7:  (1.0, 1.5),
    11: (1.0, 0.0),
}

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
    m4 = {1: new_bucket(), 3: new_bucket()}
    m3 = {1: new_bucket(), 2: new_bucket()}
    m12 = {a: new_bucket() for a in CL12}
    vsum = {a: [0, 0] for a in CL12}

    for p in ps:
        if p < 5:
            continue

        m = p - 1
        a4 = p % 4
        a3 = p % 3
        a12 = p % 12

        # valuations v2 et v3 de p-1
        t = m
        v2 = 0
        while t % 2 == 0:
            v2 += 1
            t //= 2

        v3 = 0
        while t % 3 == 0:
            v3 += 1
            t //= 3

        buckets = [g, m4[a4], m3[a3]]
        if a12 in m12:
            buckets.append(m12[a12])
            vsum[a12][0] += v2
            vsum[a12][1] += v3

        for b in buckets:
            b['n'] += 1
            for u in US:
                if lp[m] <= m ** (1.0 / u):
                    b['s'][u] += 1

    return dict(g=g, m4=m4, m3=m3, m12=m12, vsum=vsum)

def main():
    t0 = time.time()

    R = {X: weigh_scale(X) for X in SCALES}
    r6 = R[1_000_000]
    r7 = R[10_000_000]

    print("[0/5] etalon global P+(p-1) <= (p-1)^(1/u) ...")
    for u in US:
        print(f"      u={u} : globale 10^7 = {prop(r7['g'], u):.5f}")
    anchor = abs(prop(r7['g'], 2) - 0.35583) < 1e-4
    print(f"      garde u=2 contre 0.35583 : {'OK' if anchor else 'ECHEC'}")

    print("[1/5] gardes deterministes (v2, v3) par classe mod 12 (10^7) ...")
    ok_v = True

    for a in CL12:
        mv2 = r7['vsum'][a][0] / r7['m12'][a]['n']
        mv3 = r7['vsum'][a][1] / r7['m12'][a]['n']
        e2, e3 = EXP_V[a]

        ok_v &= abs(mv2 - e2) < 0.02 and abs(mv3 - e3) < 0.02

        print(f"      c{a:2d} : v2 = {mv2:.4f} (attendu {e2:.1f}) ; "
              f"v3 = {mv3:.4f} (attendu {e3:.1f})")

    print("[2/5] signature : rho1 au-dessus, rho11 au-dessous ...")
    ok_o6 = 0
    ok_o7 = 0

    for u in US:
        p6 = [prop(r6['m12'][a], u) for a in ORDER]
        p7 = [prop(r7['m12'][a], u) for a in ORDER]

        # ORDER = c1, c7, c5, c11.
        # Gardes d'extremes :
        # c1 > c7, c1 > c5, c7 > c11, c5 > c11.
        c6 = [p6[0] > p6[1], p6[0] > p6[2], p6[1] > p6[3], p6[2] > p6[3]]
        c7 = [p7[0] > p7[1], p7[0] > p7[2], p7[1] > p7[3], p7[2] > p7[3]]

        ok_o6 += sum(c6)
        ok_o7 += sum(c7)

        print(f"      u={u} : 10^7 rho(c1/c7/c5/c11) = " +
              " / ".join(f"{x:.5f}" for x in p7) +
              f" | c7 vs c5 : {'c7' if p7[1] > p7[2] else 'c5'}")

    print(f"      ordre des extremes 16/16 : 10^6 {ok_o6}/16 , 10^7 {ok_o7}/16")

    print("[3/5] multiplicativite D12 = D4 * D3 (capture authentique) ...")
    ok_m6 = 0
    ok_m7 = 0

    for u in US:
        for a in CL12:
            for (rr, tag) in ((r6, '6'), (r7, '7')):
                p12 = prop(rr['m12'][a], u)
                pg = prop(rr['g'], u)
                p4 = prop(rr['m4'][a % 4], u)
                p3 = prop(rr['m3'][a % 3], u)

                d12 = p12 / pg
                dpr = (p4 / pg) * (p3 / pg)

                # Budget sigma approximatif sur log(D12/(D4D3)).
                # Il sert de garde expérimental, pas de théorème asymptotique.
                var = sum((1 - x) / (x * n) for x, n in (
                    (p12, rr['m12'][a]['n']),
                    (p4,  rr['m4'][a % 4]['n']),
                    (p3,  rr['m3'][a % 3]['n']),
                    (pg,  rr['g']['n']),
                ))

                z = abs(math.log(d12 / dpr)) / math.sqrt(var)

                if z < 3.0:
                    if tag == '6':
                        ok_m6 += 1
                    else:
                        ok_m7 += 1

                if tag == '7':
                    print(f"      u={u} c{a:2d} : D12 = {d12:.4f} , "
                          f"D4*D3 = {dpr:.4f} , z = {z:.2f}")

    print(f"      dans 3 sigma : 10^6 {ok_m6}/16 , 10^7 {ok_m7}/16")

    print("[4/5] aveugle global/classe : direction et persistence ...")
    ok_bl = True

    for u in US:
        b6 = prop(r6['g'], u) / prop(r6['m12'][1], u)
        B6 = prop(r6['g'], u) / prop(r6['m12'][11], u)
        b7 = prop(r7['g'], u) / prop(r7['m12'][1], u)
        B7 = prop(r7['g'], u) / prop(r7['m12'][11], u)

        ok_bl &= b6 < 1 < B6 and b7 < 1 < B7

        print(f"      u={u} : 10^6 c1 {b6:.4f} c11 {B6:.4f} | "
              f"10^7 c1 {b7:.4f} c11 {B7:.4f}")

    gap6 = prop(r6['m12'][1], 2) - prop(r6['m12'][11], 2)
    gap7 = prop(r7['m12'][1], 2) - prop(r7['m12'][11], 2)
    contr = gap6 / gap7 if gap7 > 0 else 9.9

    print(f"      ecart rho1-rho11 (u=2) : 10^6 {gap6:+.5f} -> "
          f"10^7 {gap7:+.5f} (contraction x{contr:.2f})")

    ok = (
        anchor
        and ok_v
        and ok_o6 == 16
        and ok_o7 == 16
        and ok_m6 >= 15
        and ok_m7 >= 15
        and ok_bl
        and contr >= 1.05
    )

    print(f"[verdict] obstruction mod 12 : {'VERT' if ok else 'REFUSE'}")
    print(f"[OK] {time.time() - t0:.1f} s")

    hunt_log.log_scan("obstruction-mod12-mrule", 4 if ok else 0, 0 if ok else 1,
                      scanner="obstruction_mod12",
                      notes=f"m-rule anchor:{anchor} ord:{ok_o6}/{ok_o7} "
                            f"mul:{ok_m6}/{ok_m7} contr:{contr:.2f}")

if __name__ == "__main__":
    main()