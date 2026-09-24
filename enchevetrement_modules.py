#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# =============================================================================
"""
enchevetrement_modules.py v2 — Addendum XLIII : universalité de l'enchevêtrement.

Refus publiés (v1) :
  (1) ZeroDivisionError : la classe c1 mod 2^j EST la strate dyadique k >= j ;
      les strates k=1,2 y sont vides, la comparaison intra-classe contre k=1
      est impossible. Le test v1 était dégénéré (modules = strates emboîtées).
  (2) Garde G0 mal spécifiée : 0,3558 est la poignée de main de l'Addendum XVI
      (règle individuelle), pas un échec contre 0,41 (règle cumulative, XXXIII).

Question v2 : l'enchevêtrement dyadique (m = (p-1)/2^k plus lisse en profondeur
k >= 5, à u=5, en règle propre P+(m) <= m^{1/5}) survit-il au conditionnement
par des congruences IMPAIRES (mod 3, mod 5), qui ne contraignent pas v2(p-1) ?

Gardes pré-enregistrées (v2) :
  G0  : densité règle individuelle (u=2) dans [0,345 ; 0,365] (XVI : 0,3558)
        ET densité règle cumulative (u=2) dans [0,395 ; 0,425] (XXXIII : 0,41).
  G1  : strates dyadiques = 2^-k, |z| <= 4.
  G2a : z(k>=5 vs k=1, u=5, règle propre, poolé) > +3.
  G2b : z > 0 dans les 6 classes impaires (1,2 mod 3 ; 1,2,3,4 mod 5),
        dont >= 4 avec z >= +2 -> universalité ; sinon ouverture.
  G3  : marge propre c1 mod 64 à u=5 dans [+40 % ; +100 %] (ancre XLII : +73 %).
"""
import sys
import time
import math
import numpy as np

X_MAX = 10 ** 7


def crible_premiers_gpf(n):
    gpf = np.zeros(n + 1, dtype=np.int32)
    for i in range(2, n + 1):
        if gpf[i] == 0:
            gpf[i::i] = i
    is_prime = (gpf == np.arange(n + 1, dtype=np.int32))
    is_prime[0] = False
    is_prime[1] = False
    return is_prime, gpf


def main():
    t0 = time.time()
    print("=" * 70)
    print("enchevetrement_modules.py v2 — Addendum XLIII : universalite")
    print("=" * 70)
    print()
    print(f"Crible jusqu'a {X_MAX} ...")
    tc = time.time()
    is_prime, gpf = crible_premiers_gpf(X_MAX)
    print(f"Crible pret en {time.time() - tc:.1f} s")
    print()

    premiers = np.nonzero(is_prime)[0]
    premiers = premiers[premiers >= 3]
    pm1 = premiers - 1
    n_tot = len(premiers)

    low = pm1 & (-pm1)
    kvals = np.log2(low).astype(np.int64)
    m_imp = pm1 >> kvals
    gpf_m = gpf[m_imp]
    gpf_pm1 = gpf[pm1]

    # ---------------- G0 : double poignée de main ----------------
    dens_ind = float(np.count_nonzero(gpf_pm1 <= pm1 ** 0.5) / n_tot)
    dens_cum = float(np.count_nonzero(gpf_pm1 <= X_MAX ** 0.5) / n_tot)
    g0a = 0.345 <= dens_ind <= 0.365
    g0b = 0.395 <= dens_cum <= 0.425
    print(f"G0 regle individuelle (u=2) : {dens_ind:.4f} (XVI : 0,3558) -> {'OK' if g0a else 'ECHEC'}")
    print(f"G0 regle cumulative  (u=2) : {dens_cum:.4f} (XXXIII : 0,41) -> {'OK' if g0b else 'ECHEC'}")
    print()

    # ---------------- G1 : géométrie dyadique ----------------
    strate = np.where(kvals >= 5, 5, kvals)
    print("G1 geometrie dyadique (loi 2^-k) :")
    g1_ok = True
    for s in [1, 2, 3, 4, 5]:
        n_s = int(np.count_nonzero(strate == s))
        obs = n_s / n_tot
        exp = 0.5 ** s if s <= 4 else 0.5 ** 4
        sig = math.sqrt(exp * (1.0 - exp) / n_tot)
        z = (obs - exp) / sig
        ok = abs(z) <= 4.0
        g1_ok = g1_ok and ok
        lab = f"k={s}" if s <= 4 else "k>=5"
        print(f"  {lab:>5} : n = {n_s:>7}  obs = {obs:.5f}  exp = {exp:.5f}"
              f"  z = {z:+.2f} -> {'OK' if ok else 'ECHEC'}")
    print()

    # ---------------- G2 : profondeur et universalité ----------------
    def prop_u5(mask):
        nn = int(np.count_nonzero(mask))
        if nn == 0:
            return None, 0
        val = float(np.count_nonzero(gpf_m[mask] <= m_imp[mask] ** 0.2) / nn)
        return val, nn

    m_k1 = (kvals == 1)
    m_k5 = (kvals >= 5)

    classes = [("pool", np.ones(n_tot, dtype=bool))]
    classes += [(f"mod3={a}", premiers % 3 == a) for a in (1, 2)]
    classes += [(f"mod5={a}", premiers % 5 == a) for a in (1, 2, 3, 4)]

    print("G2 enchevetrement a u=5 (regle propre), k>=5 vs k=1 :")
    print(f"  {'Classe':<9} | {'n(k=1)':<8} | {'n(k>=5)':<8} | {'p(k=1)':<9} | {'p(k>=5)':<9} | z")
    print("-" * 72)
    zs = {}
    for nom, mc in classes:
        p1, n1 = prop_u5(mc & m_k1)
        p5, n5 = prop_u5(mc & m_k5)
        if p1 is None or p5 is None or n1 < 100 or n5 < 100:
            print(f"  {nom:<9} | echantillon insuffisant")
            continue
        sig = math.sqrt(p1 * (1.0 - p1) / n1 + p5 * (1.0 - p5) / n5)
        z = (p5 - p1) / sig if sig > 0 else 0.0
        zs[nom] = z
        print(f"  {nom:<9} | {n1:<8} | {n5:<8} | {p1:<9.5f} | {p5:<9.5f} | {z:+.2f}")
    print()

    z_pool = zs.get("pool", 0.0)
    g2a = z_pool > 3.0
    print(f"G2a profondeur poolée : z = {z_pool:+.2f} (> +3) -> {'OK' if g2a else 'ECHEC'}")
    impaires = [z for nom, z in zs.items() if nom != "pool"]
    n_pos2 = sum(1 for z in impaires if z >= 2.0)
    g2b = len(impaires) == 6 and all(z > 0 for z in impaires) and n_pos2 >= 4
    print(f"G2b universalité : {len([z for z in impaires if z > 0])}/6 z > 0,"
          f" {n_pos2}/6 z >= +2 -> {'OK' if g2b else 'OUVERTURE'}")
    print()

    # ---------------- G3 : poignée de main XLII ----------------
    mc64 = (premiers % 64) == 1
    p_c1, n_c1 = prop_u5(mc64)
    p_glob, n_glob = prop_u5(np.ones(n_tot, dtype=bool))
    marge = (p_c1 / p_glob - 1.0) * 100.0 if p_glob > 0 else 0.0
    g3 = 40.0 <= marge <= 100.0
    print(f"G3 marge propre c1 mod 64 (u=5) : {marge:+.1f} % (ancre XLII : +73 %)"
          f" -> {'OK' if g3 else 'ECHEC'}")
    print()

    if g0a and g0b and g1_ok and g2a and g3:
        if g2b:
            print("VERDICT : AUDIT VERT — UNIVERSALITE TENUE :")
            print("  l'enchevêtrement dyadique survit à toutes les congruences impaires testées.")
        else:
            print("VERDICT : AUDIT VERT — UNIVERSALITE PARTIELLE (ouverture mesurée) :")
            print("  l'enchevêtrement poolé tient, mais certaines classes impaires divergent.")
    else:
        print("VERDICT : ECHEC DE GARDE")
    print(f"\nTemps total : {time.time() - t0:.2f} s")
    print("[OK]")


if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    main()