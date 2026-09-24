#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# Non-commercial use only. Commercial use prohibited without written consent.
# =============================================================================
"""
grammaire_dyadique.py — Addendum XLII. Compagnon n.31.
Voie B : la grammaire dyadique — décomposition de l'amplification mod 64.

Question : l'amplification extrême de c1 mod 64 (+824 % à u=5, Addendum XXII)
est-elle un pur effet mécanique (volume 2-adique forcé + relâchement du seuil
sur p−1 = 2^k·m), ou la partie impaire m = (p−1)/2^k porte-t-elle un
ENCHEVÊTREMENT dyadique (m d'autant plus lisse que k est grand) ?

Clé structurelle : P+(p−1) = P+(m). La règle ancienne P+(p−1) <= (p−1)^{1/u}
relâche le seuil sur m d'un facteur 2^{k/u} (effet mécanique). La règle propre
P+(m) <= m^{1/u} isole l'enchevêtrement.

Protocole :
  - Crible GPF jusqu'à X = 10^7.
  - Pour chaque premier p >= 3 : k = v2(p−1), m = (p−1) >> k.
  - Strates dyadiques k = 1, 2, 3, 4, k >= 5.
  - Par strate et par u in {2, 3} : proportion de m lisses en règle propre
    et en règle ancienne.
  - Poignée de main Addendum XXII : marge de c1 mod 64 en règle ancienne, u=5.

Gardes pré-enregistrées :
  G0 (géométrie) : proportion de la strate k = 2^{-k} (queue k>=5 = 2^{-4}),
     à 4 sigma binomiaux près.
  G1 (poignée XXII) : marge c1 mod 64 (règle ancienne, u=5) dans [+600, +1000] %.
  G2 (enchevêtrement) : z-scores des strates k=2,3,4,>=5 contre la strate 1,
     en règle propre, |z| <= 3 partout -> INDÉPENDANCE ; sinon ENCHEVÊTREMENT.
  G3 (décomposition) : table règle ancienne vs règle propre sur c1 mod 64,
     descriptive, sans seuil.
"""
import sys
import time
import math
import numpy as np

X_MAX = 10 ** 7
US = [2, 3]


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
    print("grammaire_dyadique.py — Addendum XLII : la grammaire dyadique")
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

    low = pm1 & (-pm1)                      # plus grande puissance de 2 | p−1
    kvals = np.log2(low).astype(np.int64)   # valuation 2-adique k
    m_imp = pm1 >> kvals                    # partie impaire m
    gpf_m = gpf[m_imp]
    gpf_pm1 = gpf[pm1]
    strate = np.where(kvals >= 5, 5, kvals)

    # ---------------- G0 : géométrie dyadique ----------------
    print("G0 geometrie dyadique (loi geometrique 2^-k) :")
    g0_ok = True
    ns = {}
    for s in [1, 2, 3, 4, 5]:
        n_s = int(np.count_nonzero(strate == s))
        ns[s] = n_s
        obs = n_s / n_tot
        exp = 0.5 ** s if s <= 4 else 0.5 ** 4
        sig = math.sqrt(exp * (1.0 - exp) / n_tot)
        z = (obs - exp) / sig
        ok = abs(z) <= 4.0
        g0_ok = g0_ok and ok
        lab = f"k={s}" if s <= 4 else "k>=5"
        print(f"  {lab:>5} : n = {n_s:>7}  obs = {obs:.5f}  exp = {exp:.5f}"
              f"  z = {z:+.2f} -> {'OK' if ok else 'ECHEC'}")
    print()

    # ---------- proportions par strate, deux règles ----------
    props_m = {}
    props_old = {}
    for s in [1, 2, 3, 4, 5]:
        msk = strate == s
        mm = m_imp[msk]
        pp = pm1[msk]
        gm = gpf_m[msk]
        gp = gpf_pm1[msk]
        for u in US:
            props_m[(s, u)] = float(np.count_nonzero(gm <= mm ** (1.0 / u)) / ns[s])
            props_old[(s, u)] = float(np.count_nonzero(gp <= pp ** (1.0 / u)) / ns[s])
    print("Strates dyadiques : lissite de m (regle propre) vs de p-1 (regle ancienne) :")
    for u in US:
        print(f"  u = {u} :")
        for s in [1, 2, 3, 4, 5]:
            lab = f"k={s}" if s <= 4 else "k>=5"
            print(f"    {lab:>5} : n = {ns[s]:>7}  m lisse = {props_m[(s, u)]:.5f}"
                  f"  p-1 lisse = {props_old[(s, u)]:.5f}")
    print()

    # ---------------- G2 : enchevêtrement ----------------
    print("G2 enchevêtrement dyadique (z vs strate 1, regle propre) :")
    g2_ok = True
    for u in US:
        p1 = props_m[(1, u)]
        for s in [2, 3, 4, 5]:
            ps = props_m[(s, u)]
            sig = math.sqrt(p1 * (1.0 - p1) / ns[s] + p1 * (1.0 - p1) / ns[1])
            z = (ps - p1) / sig if sig > 0 else 0.0
            ok = abs(z) <= 3.0
            g2_ok = g2_ok and ok
            lab = f"k={s}" if s <= 4 else "k>=5"
            print(f"  u={u} {lab:>5} : {ps:.5f} vs {p1:.5f}  z = {z:+.2f}"
                  f" -> {'OK' if ok else 'SIGNAL'}")
    print()

    # ------- G1 + G3 : poignée de main XXII et décomposition -------
    msk_c1 = (premiers % 64) == 1
    n_c1 = int(np.count_nonzero(msk_c1))
    print(f"G1/G3 classe c1 mod 64 : n = {n_c1}")
    g1_ok = True
    for u in [2, 5]:
        pp = pm1[msk_c1]
        gp = gpf_pm1[msk_c1]
        prop_c1 = float(np.count_nonzero(gp <= pp ** (1.0 / u)) / n_c1)
        prop_g = float(np.count_nonzero(gpf_pm1 <= pm1 ** (1.0 / u)) / n_tot)
        marg = (prop_c1 / prop_g - 1.0) * 100.0
        if u == 5:
            ok = 600.0 <= marg <= 1000.0
            g1_ok = g1_ok and ok
            print(f"  G1 u=5 : marge c1 = {marg:+.1f} % (ancre +824 %)"
                  f" -> {'OK' if ok else 'ECHEC'}")
        else:
            print(f"  rappel u=2 : marge c1 = {marg:+.1f} % (Addendum XXII : +77,7 %)")
    print("G3 decomposition c1 mod 64 (mecanique vs enchevêtrement) :")
    for u in [2, 3, 5]:
        pp = pm1[msk_c1]
        gp = gpf_pm1[msk_c1]
        mm = m_imp[msk_c1]
        gm = gpf_m[msk_c1]
        prop_c1_old = float(np.count_nonzero(gp <= pp ** (1.0 / u)) / n_c1)
        prop_g_old = float(np.count_nonzero(gpf_pm1 <= pm1 ** (1.0 / u)) / n_tot)
        marg_old = (prop_c1_old / prop_g_old - 1.0) * 100.0
        prop_c1_m = float(np.count_nonzero(gm <= mm ** (1.0 / u)) / n_c1)
        prop_g_m = float(np.count_nonzero(gpf_m <= m_imp ** (1.0 / u)) / n_tot)
        marg_m = (prop_c1_m / prop_g_m - 1.0) * 100.0
        print(f"  u={u} : ancienne = {marg_old:+7.1f} % | propre = {marg_m:+6.1f} %"
              f" | mecanique = {marg_old - marg_m:+7.1f} pts")
    print()

    if g0_ok and g1_ok and g2_ok:
        print("VERDICT : AUDIT VERT — INDEPENDANCE : le +824 % est un volume")
        print("  mecanique (2-adique + seuil) ; la partie impaire ne porte rien.")
    elif g0_ok and g1_ok:
        print("VERDICT : AUDIT VERT — ENCHEVÊTREMENT DYADIQUE DETECTE :")
        print("  la partie impaire m est plus lisse aux grandes profondeurs 2-adiques.")
        print("  Ouverture majeure (structure au-dela du volume).")
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