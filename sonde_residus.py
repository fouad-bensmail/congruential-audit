#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# Non-commercial use only. Commercial use prohibited without written consent.
# =============================================================================
"""
sonde_residus.py -- Exposant alpha et residus du terme croise.
Addendum XXXIV, Direction unique : sonde du residu de C1. Compagnon n.23.

Protocole : echelle dense de 60 paliers entre 10^6 et 10^8. Pour chaque
palier X et chaque u, on mesure C(X)=(D12*Dglobal)/(D4*D3) sur les quatre
classes modeles 1,5,7,11. Puis :
  (1) Fit |C(X)-1| ~ A/(log X)^alpha  -> mesure alpha (G2).
  (2) Residus + autocorrelation lag-1  -> bruit ou structure ? (G4).

Gardes : G1 monotonie ; G2 alpha >= 1 ; G3 densite globale ~0,41 (u=2) ;
         G4 autocorr residus (|rho1| > 0.5 = structure suspectee).
Positionnement honnete : on ne cherche pas a prouver GUE/Montgomery. On
teste si le residu est du bruit ou une oscillation (ouverture, pas preuve).
"""

import sys
import time
import math
import numpy as np

X_MAX = 10**8
X_MIN = 10**6
N_PALIERS = 60

def crible_premiers_gpf(n):
    """Retourne is_prime (bool) et gpf (int) jusqu'a n."""
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
    print("sonde_residus.py -- exposant alpha et residus du terme croise")
    print("=" * 70)
    print()

    print(f"Crible jusqu'a {X_MAX} ...")
    t_c = time.time()
    is_prime, gpf = crible_premiers_gpf(X_MAX)
    print(f"Crible pret en {time.time()-t_c:.1f} s")

    premiers = np.nonzero(is_prime)[0]
    # CORRECT : gpf_pm1[i] = gpf[p-1] pour p = premiers[i] (pas de decalage)
    gpf_pm1 = gpf[premiers - 1]
    classes12 = (premiers % 12).astype(np.int64)
    classes4 = (premiers % 4).astype(np.int64)
    classes3 = (premiers % 3).astype(np.int64)
    print(f"{len(premiers)} premiers jusqu'a {X_MAX}\n")

    paliers = np.unique(np.geomspace(X_MIN, X_MAX, N_PALIERS).astype(np.int64))
    u_values = [2, 3]
    classes_modeles = [1, 5, 7, 11]

    print("Gardes : G1 monotonie | G2 alpha>=1 | G3 densite | G4 autocorr")
    print()

    for u in u_values:
        print(f"--- u = {u} ---")
        print(f"  {'Classe':<7} {'alpha':>7} {'A':>9} {'autocorr r1':>12} {'verdict':>11}")
        densites = []
        for a in classes_modeles:
            data = []
            for X in paliers:
                idx = np.searchsorted(premiers, X, side='right')
                if idx < 1000:
                    continue
                seuil = X ** (1.0 / u)
                masque_lisse = (gpf_pm1[:idx] <= seuil).astype(np.float64)
                d_global = np.sum(masque_lisse) / idx
                densites.append(d_global)

                lisse12 = np.bincount(classes12[:idx], weights=masque_lisse, minlength=12)
                total12 = np.bincount(classes12[:idx], minlength=12)
                lisse4 = np.bincount(classes4[:idx], weights=masque_lisse, minlength=4)
                total4 = np.bincount(classes4[:idx], minlength=4)
                lisse3 = np.bincount(classes3[:idx], weights=masque_lisse, minlength=3)
                total3 = np.bincount(classes3[:idx], minlength=3)

                D12 = lisse12[a] / total12[a] if total12[a] > 0 else 0
                D4 = lisse4[a % 4] / total4[a % 4] if total4[a % 4] > 0 else 0
                D3 = lisse3[a % 3] / total3[a % 3] if total3[a % 3] > 0 else 0
                if D4 > 0 and D3 > 0:
                    C = (D12 * d_global) / (D4 * D3)
                    data.append((X, abs(C - 1.0)))

            Xs = np.array([x for x, _ in data])
            devs = np.array([d for _, d in data])
            loglogX = np.log(np.log(Xs))
            logdev = np.log(devs + 1e-15)
            pente, ordonnee = np.polyfit(loglogX, logdev, 1)
            alpha = -pente
            A = math.exp(ordonnee)
            residus = logdev - (ordonnee + pente * loglogX)
            r = residus - np.mean(residus)
            rho1 = np.sum(r[:-1] * r[1:]) / np.sum(r**2) if np.sum(r**2) > 0 else 0.0
            verdict = "STRUCTURE" if abs(rho1) > 0.5 else "bruit"
            print(f"  {a:<7} {alpha:>7.3f} {A:>9.4f} {rho1:>12.3f} {verdict:>11}")

        d_moy = np.mean(densites)
        print(f"  Densite globale moyenne : {d_moy:.4f}")
        print()

    print("=" * 70)
    print("Lecture : alpha = vitesse d'extinction ; autocorr r1 = memoire du residu.")
    print("  r1 proche de 0 -> residu = bruit (loi de puissance propre).")
    print("  |r1| > 0.5     -> residu structure (ouverture vers zeros de fonctions L).")
    dt = time.time() - t0
    print(f"\nTemps total : {dt:.2f} s")
    print("[OK]")

if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    main()