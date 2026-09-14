#!/usr/bin/env python3
"""
terme_croise.py — la loi de composition des obstructions, au bon niveau.

Lecon du refus mod12-mrule : les ratios ne multiplient pas (Dickman n'est pas
exponentielle) ; ce sont les DECALAGES en u qui s'additionnent.
Trois peses :
  [1] solveur de Dickman : u.rho'(u) = -rho(u-1), garde contre la table
      (rho(2), rho(3), rho(4) = 0.30685 / 0.04861 / 0.00497) ;
  [2] additivite des decalages : s4 et s3 extraits des classes solos par
      inversion de rho, prediction D12 = rho(u-s4-s3)/rho(u) comparee a la
      mesure, budget 4 sigma en u=2,3 a 10^7 ;
  [3] terme croise C = D12/(D4*D3) : table aux deux echelles, motif de signes
      (extremes < 1, medianes > 1, predit par la log-convexite de rho) et
      contraction de |C-1| entre 10^6 et 10^7 attendue ~ (16,1/13,8)^2 = 1,36
      (fenetre [1,1 ; 1,7]) si le residu est en 1/ln X ;
  u=4,5 rapportes comme mesure pure (matiere d'addendum).
Regle de lissite validee : P+(m) <= m^(1/u).
Usage : python -u terme_croise.py
"""
import math, time
from array import array
import hunt_log

US = (2, 3, 4, 5)
UGAR = (2, 3)
SCALES = (1_000_000, 10_000_000)
CL12 = (1, 5, 7, 11)

def primes_to(n):
    c = bytearray([1]) * (n + 1)
    c[0:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if c[i]:
            c[i*i:n+1:i] = bytearray(len(range(i*i, n+1, i)))
    return [i for i in range(2, n + 1) if c[i]]

def lpf_sieve(X):
    lp = array('I', [0]) * (X + 1)
    for p in range(2, X + 1):
        if lp[p] == 0:
            lp[p::p] = array('I', [p]) * len(range(p, X + 1, p))
    return lp

def build_rho(umax=6.0, h=1e-5):
    n = int(umax / h) + 2
    r = [1.0] * (n + 1)
    k1 = int(1.0 / h)
    for i in range(k1, n):
        u = i * h
        r[i+1] = r[i] - h * r[i - k1] / u
    return r, h

def rho_of(r, h, x):
    if x <= 0.0:
        return 1.0
    i = int(x / h)
    if i + 1 >= len(r):
        return r[-1]
    f = x / h - i
    return r[i] * (1 - f) + r[i+1] * f

def rho_inv(r, h, v):
    lo, hi = 0.5, 9.0
    for _ in range(90):
        mid = 0.5 * (lo + hi)
        if rho_of(r, h, mid) > v:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

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
    for p in ps:
        if p < 5:
            continue
        m = p - 1
        a4, a3, a12 = p % 4, p % 3, p % 12
        sm = [lp[m] <= m ** (1.0 / u) for u in US]
        buckets = (g, m4[a4], m3[a3]) + ((m12[a12],) if a12 in m12 else ())
        for b in buckets:
            b['n'] += 1
            for i, u in enumerate(US):
                if sm[i]:
                    b['s'][u] += 1
    return dict(g=g, m4=m4, m3=m3, m12=m12)

def main():
    t0 = time.time()
    R = {X: weigh_scale(X) for X in SCALES}
    r6, r7 = R[1_000_000], R[10_000_000]
    rho, h = build_rho()

    print("[1/3] solveur de Dickman contre la table ...")
    tab = (0.30685, 0.04861, 0.00497)
    ok_rho = True
    for j, u in enumerate((2, 3, 4)):
        v = rho_of(rho, h, float(u))
        ok_rho &= abs(v - tab[j]) < 2e-4
        print(f"      rho({u}) = {v:.5f} (table {tab[j]:.5f})")

    print("[2/3] additivite des decalages s12 = s4 + s3 (10^7, u=2,3) ...")
    ok_add = True
    for u in UGAR:
        pg = prop(r7['g'], u)
        for a in CL12:
            d4 = prop(r7['m4'][a % 4], u) / pg
            d3 = prop(r7['m3'][a % 3], u) / pg
            s4 = u - rho_inv(rho, h, d4 * rho_of(rho, h, float(u)))
            s3 = u - rho_inv(rho, h, d3 * rho_of(rho, h, float(u)))
            pred = rho_of(rho, h, u - s4 - s3) / rho_of(rho, h, float(u))
            mes = prop(r7['m12'][a], u) / pg
            p12 = prop(r7['m12'][a], u)
            var = sum((1 - x) / (x * n) for x, n in (
                (p12, r7['m12'][a]['n']),
                (prop(r7['m4'][a % 4], u), r7['m4'][a % 4]['n']),
                (prop(r7['m3'][a % 3], u), r7['m3'][a % 3]['n']),
                (pg, r7['g']['n'])))
            z = abs(math.log(mes / pred)) / math.sqrt(var)
            ok_add &= z < 4.0
            print(f"      u={u} c{a:2d} : s4={s4:+.4f} s3={s3:+.4f} "
                  f"pred={pred:.4f} mes={mes:.4f} z={z:.2f}")

    print("[3/3] terme croise C = D12/(D4*D3) : signes et contraction ...")
    ok_sig = True
    dev6 = []
    dev7 = []
    for u in US:
        line = f"      u={u} :"
        for (rr, tag, acc) in ((r6, '6', dev6), (r7, '7', dev7)):
            pg = prop(rr['g'], u)
            cs = []
            for a in CL12:
                d12 = prop(rr['m12'][a], u) / pg
                dpr = (prop(rr['m4'][a % 4], u) / pg) * \
                      (prop(rr['m3'][a % 3], u) / pg)
                C = d12 / dpr
                cs.append(C)
                if u in UGAR:
                    acc.append(abs(C - 1.0))
                    want_lt = a in (1, 11)
                    ok_sig &= (C < 1.0) if want_lt else (C > 1.0)
            line += f" 10^{tag} " + "/".join(f"{c:.4f}" for c in cs)
        print(line + "   (c1/c5/c7/c11)")
    m6 = sum(dev6) / len(dev6)
    m7 = sum(dev7) / len(dev7)
    contr = m6 / m7 if m7 > 0 else 9.9
    print(f"      |C-1| moyen (u=2,3) : 10^6 {m6:.5f} -> 10^7 {m7:.5f} "
          f"(contraction x{contr:.2f}, attendu ~1,36)")
    ok_contr = 1.1 <= contr <= 1.7

    ok = ok_rho and ok_add and ok_sig and ok_contr
    print(f"[verdict] terme croise : {'VERT' if ok else 'REFUSE'}")
    print(f"[OK] {time.time() - t0:.1f} s")
    hunt_log.log_scan("terme-croise", 4 if ok else 0, 0 if ok else 1,
                      scanner="terme_croise",
                      notes=f"rho:{ok_rho} add:{ok_add} sig:{ok_sig} "
                            f"contr:{contr:.2f}")

if __name__ == "__main__":
    main()