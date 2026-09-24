#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# =============================================================================
"""
carte_dyadique.py v3 — Addendum XLIV. Compagnon n.33.
Direction déclarée : tracer les espaces des motifs.
La carte dyadique de l'enchevêtrement sur l'espace des structures.
"""
import sys
import time
import math
import numpy as np

X_MAX = 10 ** 8
U_PRIM = 4
U_CONF = 5
QS = (3, 5, 7, 11, 13)

def crible_gpf(n):
    gpf = np.zeros(n + 1, dtype=np.int32)
    for i in range(2, n + 1):
        if gpf[i] == 0:
            gpf[i::i] = i
    return gpf

def ratio_strates(gpf, m, k, mask, u):
    m1 = mask & (k == 1)
    m5 = mask & (k >= 5)
    n1 = int(np.count_nonzero(m1))
    n5 = int(np.count_nonzero(m5))
    if n1 < 200 or n5 < 200:
        return None
    a1 = m[m1]
    a5 = m[m5]
    p1 = float(np.count_nonzero(gpf[a1] <= a1 ** (1.0 / u)) / n1)
    p5 = float(np.count_nonzero(gpf[a5] <= a5 ** (1.0 / u)) / n5)
    se = math.sqrt(p1 * (1.0 - p1) / n1 + p5 * (1.0 - p5) / n5)
    z = (p5 - p1) / se if se > 0 else 0.0
    return {"R": (p5 / p1 if p1 > 0 else float("nan")), "z": z,
            "n1": n1, "n5": n5, "p1": p1, "p5": p5}

def main():
    t0 = time.time()
    print("=" * 78)
    print("carte_dyadique.py v3 — Addendum XLIV : la carte dyadique des motifs")
    print("=" * 78)
    print()
    print(f"Crible GPF jusqu'a {X_MAX} ...")
    tc = time.time()
    gpf = crible_gpf(X_MAX)
    is_prime = (gpf == np.arange(X_MAX + 1, dtype=np.int32))
    is_prime[0] = False
    is_prime[1] = False
    print(f"Crible pret en {time.time() - tc:.1f} s")
    print()

    premiers = np.nonzero(is_prime)[0]
    premiers = premiers[premiers >= 3]
    pm1 = premiers - 1
    low = pm1 & (-pm1)
    k = np.log2(low).astype(np.int64)
    m = pm1 >> k
    n_tot = len(premiers)
    print(f"Premiers >= 3 : {n_tot}")
    print()

    lignes = []

    def ajoute(nom, mask, u):
        r = ratio_strates(gpf, m, k, mask, u)
        if r is not None:
            lignes.append((nom, u, r))
        return r

    ones = np.ones(n_tot, dtype=bool)

    mtw = (premiers + 2 <= X_MAX) & is_prime[np.minimum(premiers + 2, X_MAX)]
    n_tw = int(np.count_nonzero(mtw))
    print("G0 geometrie dyadique dans les jumeaux :")
    g0_ok = True
    for s in [1, 2, 3, 4, 5]:
        if s <= 4:
            obs = float(np.count_nonzero(mtw & (k == s)) / n_tw)
            exp = 0.5 ** s
        else:
            obs = float(np.count_nonzero(mtw & (k >= 5)) / n_tw)
            exp = 0.5 ** 4
        sig = math.sqrt(exp * (1.0 - exp) / n_tw)
        z = (obs - exp) / sig
        ok = abs(z) <= 4.0
        g0_ok = g0_ok and ok
        lab = f"k={s}" if s <= 4 else "k>=5"
        print(f"  {lab:>5} : obs = {obs:.5f}  exp = {exp:.5f}  z = {z:+.2f} -> {'OK' if ok else 'ECHEC'}")
    print()

    r_g4 = ajoute("global", ones, U_PRIM)
    ajoute("global", ones, U_CONF)
    print(f"Ancre globale : R(u=4) = {r_g4['R']:.3f} (z = {r_g4['z']:+.2f})")
    print()

    print("Axe 1 — loi du couplage (classes c1 mod q, u=4) :")
    print(f"  {'q':<4} | {'R brute':<9} | {'R propre':<9} | {'z propre':<9} | mecanique")
    r_prop = {}
    g1_ok = True
    for q in QS:
        mq = (premiers % q) == 1
        r_raw = ratio_strates(gpf, m, k, mq, U_PRIM)
        n_forc = int(np.count_nonzero(mq & (m % q != 0)))
        m2 = m // q
        m1 = mq & (k == 1)
        m5 = mq & (k >= 5)
        n1 = int(np.count_nonzero(m1))
        n5 = int(np.count_nonzero(m5))
        a1 = m2[m1]
        a5 = m2[m5]
        p1 = float(np.count_nonzero(gpf[a1] <= a1 ** (1.0 / U_PRIM)) / n1)
        p5 = float(np.count_nonzero(gpf[a5] <= a5 ** (1.0 / U_PRIM)) / n5)
        se = math.sqrt(p1 * (1.0 - p1) / n1 + p5 * (1.0 - p5) / n5)
        z = (p5 - p1) / se if se > 0 else 0.0
        rp = p5 / p1 if p1 > 0 else float("nan")
        r_prop[q] = (rp, z)
        mec = (r_raw["R"] / rp) if (rp == rp and rp > 0) else float("nan")
        print(f"  {q:<4} | {r_raw['R']:<9.3f} | {rp:<9.3f} | {z:+8.2f}  | {mec:.3f}  (q|m non forces: {n_forc})")
        if q in (3, 5):
            g1_ok = g1_ok and (z >= 2.0)
    r3, z3 = r_prop[3]
    r13, z13 = r_prop[13]
    se3 = (r3 - 1.0) / z3 if z3 > 0 else 1e-9
    se13 = (r13 - 1.0) / z13 if z13 > 0 else 1e-9
    z_ext = (r3 - r13) / math.sqrt(se3 ** 2 + se13 ** 2)
    g1_ok = g1_ok and (z_ext >= 2.0)
    print(f"  loi des extremes R_prop(3) > R_prop(13) : z = {z_ext:+.2f} -> {'OK' if z_ext >= 2.0 else 'ECHEC'}")
    print()

    print("Axe 2 — famille Sophie Germain (p < 5e7) :")
    sub = premiers < 5 * 10 ** 7
    msg = np.zeros(n_tot, dtype=bool)
    msg[sub] = is_prime[2 * premiers[sub] + 1]
    r_sg = ajoute("sophie_germain", msg, U_PRIM)
    ajoute("sophie_germain", msg, U_CONF)
    g2_ok = (r_sg is not None) and (r_sg["z"] >= 3.0)
    print(f"  n(SG) = {int(np.count_nonzero(msg))} ; R_SG(u=4) = {r_sg['R']:.3f}"
          f"  z = {r_sg['z']:+.2f} (n1={r_sg['n1']}, n5={r_sg['n5']}) -> {'OK' if g2_ok else 'ECHEC'}")
    print()

    print("Axe 3 — espace des motifs (u=4) :")
    mcou = (premiers + 4 <= X_MAX) & is_prime[np.minimum(premiers + 4, X_MAX)]
    msex = (premiers + 6 <= X_MAX) & is_prime[np.minimum(premiers + 6, X_MAX)]
    r_tw = ajoute("jumeaux {0,2}", mtw, U_PRIM)
    ajoute("jumeaux {0,2}", mtw, U_CONF)
    r_co = ajoute("cousins {0,4}", mcou, U_PRIM)
    r_se = ajoute("sexy {0,6}", msex, U_PRIM)
    g3_ok = (r_tw is not None) and (r_tw["z"] >= 3.0)
    print(f"  R_jumeaux(u=4) = {r_tw['R']:.3f}  z = {r_tw['z']:+.2f} -> {'OK' if g3_ok else 'ECHEC'}")
    print(f"  R_cousins(u=4) = {r_co['R']:.3f}  z = {r_co['z']:+.2f} (descriptif)")
    print(f"  R_sexy(u=4)    = {r_se['R']:.3f}  z = {r_se['z']:+.2f} (descriptif)")
    print()

    print("CARTE DYADIQUE DE L'ESPACE DES STRUCTURES (R, u=4 sauf mention) :")
    print(f"  {'Structure':<18} | {'u':<3} | {'R':<8} | {'z':<8} | {'n(k=1)':<9} | n(k>=5)")
    print("-" * 74)
    for nom, u, r in lignes:
        print(f"  {nom:<18} | {u:<3} | {r['R']:<8.3f} | {r['z']:+8.2f} | {r['n1']:<9} | {r['n5']}")
    print()

    if g0_ok and g1_ok and g2_ok and g3_ok:
        print("VERDICT : AUDIT VERT — la carte dyadique est tracee sur tout l'espace.")
    else:
        print("VERDICT : ECHEC DE GARDE (la carte est publiee, les gardes nomment le refus)")
    print(f"\nTemps total : {time.time() - t0:.2f} s")
    print("[OK]")

if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    main()