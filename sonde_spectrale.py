#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# =============================================================================
"""
sonde_spectrale.py v3 — Addendum XXXVI. Compagnon n.25.
L'Echelle Spectrale : la chasse aux zeros du residu de C1.

Refus publies (v1) : regle de lissite individuelle au lieu de cumulative.
Refus publies (v2) : variable de regression incorrecte (ln X au lieu de
  ln(ln X)), et soustraction de tendance par inversion de signe.
Corrections v3 :
  (1) regression sur ln(ln X) : ln|r| = ln A - alpha * ln(ln X) ;
  (2) normalisation r / tendance au lieu de |r| - tendance ;
  (3) FFT sur le residu normalise (amplitude constante).
"""
import sys
import time
import math
import numpy as np

X_MAX = 10**8
X_MIN = 10**6
N_PALIERS = 300
US = [2, 3]
CLASSES12 = [1, 5, 7, 11]

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
    print("sonde_spectrale.py v3 — Addendum XXXVI : l'Echelle Spectrale")
    print("=" * 70)
    print()
    print(f"Crible jusqu'a {X_MAX} ...")
    t_c = time.time()
    is_prime, gpf = crible_premiers_gpf(X_MAX)
    print(f"Crible pret en {time.time()-t_c:.1f} s")
    print()

    premiers = np.nonzero(is_prime)[0]
    premiers = premiers[premiers >= 3]
    pm1 = premiers - 1
    gpf_pm1 = gpf[pm1]
    classes12 = premiers % 12
    classes4 = premiers % 4
    classes3 = premiers % 3

    logX_paliers = np.linspace(np.log(X_MIN), np.log(X_MAX), N_PALIERS)
    X_paliers = np.exp(logX_paliers)
    idx_paliers = np.searchsorted(premiers, X_paliers, side="right")
    # Variable de regression correcte : ln(ln X)
    loglogX_paliers = np.log(logX_paliers)

    g1_ok_all = True
    all_signaux = []

    for u in US:
        print(f"--- u = {u} ---")
        P_global = np.zeros(N_PALIERS)
        P12 = {a: np.zeros(N_PALIERS) for a in CLASSES12}
        P4 = {a: np.zeros(N_PALIERS) for a in [1, 3]}
        P3 = {a: np.zeros(N_PALIERS) for a in [1, 2]}

        for i in range(N_PALIERS):
            idx = idx_paliers[i]
            if idx == 0:
                continue
            seuil = X_paliers[i] ** (1.0 / u)
            gpf_pm1_i = gpf_pm1[:idx]
            lisse_i = (gpf_pm1_i <= seuil)
            n_i = float(idx)
            P_global[i] = np.sum(lisse_i) / n_i
            c12_i = classes12[:idx]
            c4_i = classes4[:idx]
            c3_i = classes3[:idx]
            for a in CLASSES12:
                mask = (c12_i == a)
                n_a = np.sum(mask)
                P12[a][i] = np.sum(lisse_i & mask) / n_a if n_a > 0 else 0.0
            for a in [1, 3]:
                mask = (c4_i == a)
                n_a = np.sum(mask)
                P4[a][i] = np.sum(lisse_i & mask) / n_a if n_a > 0 else 0.0
            for a in [1, 2]:
                mask = (c3_i == a)
                n_a = np.sum(mask)
                P3[a][i] = np.sum(lisse_i & mask) / n_a if n_a > 0 else 0.0

        dens_finale = P_global[-1]
        attendu = 0.41 if u == 2 else 0.11
        g1_ok = abs(dens_finale - attendu) < 0.08
        if not g1_ok:
            g1_ok_all = False
        print(f"  G1 densite globale finale : {dens_finale:.4f} (attendu ~{attendu}) -> {'OK' if g1_ok else 'ECHEC'}")

        for a in CLASSES12:
            q4 = a % 4
            q3 = a % 3
            num = P12[a] * P_global
            den = P4[q4] * P3[q3]
            C = num / np.maximum(den, 1e-12)
            residu = C - 1.0

            # CORRECTION v3 : regression sur ln(ln X), pas ln X
            valide = (np.abs(residu) > 1e-12) & (loglogX_paliers > 0)
            alpha = 0.0
            A = 1.0
            if np.sum(valide) > 10:
                coeffs = np.polyfit(loglogX_paliers[valide], np.log(np.abs(residu[valide])), 1)
                alpha = -coeffs[0]
                A = np.exp(coeffs[1])
                tendance = A / (logX_paliers ** alpha)
                # CORRECTION v3 : normalisation au lieu de soustraction
                residu_norm = residu / np.maximum(tendance, 1e-15)
            else:
                residu_norm = residu

            # Autocorrelation lag-1 du residu normalise
            r_centered = residu_norm - np.mean(residu_norm)
            denom = np.sum(r_centered ** 2)
            rho1 = np.sum(r_centered[:-1] * r_centered[1:]) / denom if denom > 0 else 0.0

            # FFT sur le residu normalise
            fft_vals = np.fft.fft(residu_norm)
            ds = logX_paliers[1] - logX_paliers[0]
            freqs = np.fft.fftfreq(N_PALIERS, d=ds)
            pos_mask = freqs > 0
            freqs_pos = freqs[pos_mask]
            ampl = np.abs(fft_vals[pos_mask])
            t_vals = 2 * math.pi * freqs_pos

            # Filtrage des harmoniques de fenetre
            ampl_med = np.median(ampl)
            harmoniques = [2 * math.pi * k / (N_PALIERS * ds) for k in range(1, 10)]
            pics_t = sorted(t_vals[ampl > 3 * ampl_med])
            pics_propres = []
            for t in pics_t:
                est_harmonique = any(abs(t - h) < 0.3 for h in harmoniques)
                if not est_harmonique:
                    pics_propres.append(t)

            signal = len(pics_propres) > 0
            if signal:
                all_signaux.append((u, a, pics_propres))

            print(f"  Classe {a:>2}: alpha = {alpha:.3f}, rho1 = {rho1:.3f}", end="")
            if pics_propres:
                print(f", SIGNAUX t : {', '.join(f'{t:.1f}' for t in pics_propres[:8])}")
            elif pics_t:
                print(f", pics (harmoniques) : {', '.join(f'{t:.1f}' for t in pics_t[:6])}")
            else:
                print(", aucun pic")

    dt = time.time() - t0
    print()
    if g1_ok_all:
        print("VERDICT : AUDIT VERT")
    else:
        print("VERDICT : ECHEC DE GARDE (G1 hors norme)")
    if all_signaux:
        print(f"  {len(all_signaux)} signaux detectes (hors harmoniques de fenetre)")
        for u, a, pics in all_signaux:
            print(f"    u={u}, classe {a}: t = {', '.join(f'{t:.1f}' for t in pics[:8])}")
    else:
        print("  Aucun signal spectral detecte hors harmoniques de fenetre.")
    print(f"\nTemps total : {dt:.2f} s")
    print("[OK]")

if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    main()