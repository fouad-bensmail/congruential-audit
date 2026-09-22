#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# =============================================================================
"""
spectre_etendu.py v2 — Addendum XXXVII. Compagnon n.26.
Spectre étendu : amélioration de la résolution fréquentielle du résidu de C1.

Refus publié (v1) : la régression de tendance était faite sur toute la fenêtre
[10^5, 10^8], donnant alpha ∈ [3.0, 3.6] en u=2 (hors garde G2 [1.2, 3.0]).
L'exposant effectif varie avec l'échelle : ~3 à 10^5, ~2 à 10^8.
Correction v2 : la tendance est ajustée sur la sous-fenêtre [10^6, 10^8]
(reproduction de l'Addendum XXXIV), mais appliquée à toute la fenêtre pour la FFT.
"""
import sys
import time
import math
import numpy as np

X_MAX = 10**8
X_MIN = 10**5
X_REG_MIN = 10**6  # Sous-fenêtre pour la régression de tendance
N_PALIERS = 600
US = [2, 3]
CLASSES12 = [1, 5, 7, 11]

ZETA_ZEROS = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832
]

def crible_premiers_gpf(n):
    gpf = np.zeros(n + 1, dtype=np.int32)
    for i in range(2, n + 1):
        if gpf[i] == 0:
            gpf[i::i] = i
    is_prime = (gpf == np.arange(n + 1, dtype=np.int32))
    is_prime[0] = False
    is_prime[1] = False
    return is_prime, gpf

def nearest_zero(t):
    best = min(ZETA_ZEROS, key=lambda z: abs(t - z))
    return best, abs(t - best)

def find_peaks(t_vals, ampl, t_min=4.0, thresh_factor=3.0):
    mask = t_vals >= t_min
    t = t_vals[mask]
    a = ampl[mask]
    if len(a) == 0:
        return []
    med = np.median(a)
    thresh = thresh_factor * med
    peaks = []
    for i in range(len(a)):
        if a[i] > thresh:
            left = a[i - 1] if i > 0 else -np.inf
            right = a[i + 1] if i < len(a) - 1 else -np.inf
            if a[i] >= left and a[i] >= right:
                peaks.append((float(a[i]), float(t[i])))
    peaks.sort(reverse=True)
    return peaks[:10]

def main():
    t0 = time.time()
    print("=" * 70)
    print("spectre_etendu.py v2 — Addendum XXXVII : Spectre etendu")
    print("=" * 70)
    print()

    L = math.log(X_MAX) - math.log(X_MIN)
    delta_t = 2 * math.pi / L
    print(f"Fenetre FFT : [{X_MIN:.0e}, {X_MAX:.0e}]")
    print(f"Fenetre regression : [{X_REG_MIN:.0e}, {X_MAX:.0e}]")
    print(f"Etendue logarithmique L = {L:.4f}")
    print(f"Resolution frequenteielle Delta t = {delta_t:.3f}")
    g3_ok = delta_t < 1.0
    print(f"G3 resolution Delta t < 1.0 -> {'OK' if g3_ok else 'ECHEC'}")
    print()

    print(f"Crible jusqu'a {X_MAX} ...")
    t_c = time.time()
    is_prime, gpf = crible_premiers_gpf(X_MAX)
    print(f"Crible pret en {time.time() - t_c:.1f} s")
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
    loglogX_paliers = np.log(logX_paliers)
    ds = logX_paliers[1] - logX_paliers[0]
    # Masque de sous-fenêtre pour la régression
    mask_reg_window = (X_paliers >= X_REG_MIN)

    g1_all_ok = True
    g2_all_ok = True
    zeta_matches = []

    for u in US:
        print(f"--- u = {u} ---")
        P_global = np.zeros(N_PALIERS)
        P12 = {a: np.zeros(N_PALIERS) for a in CLASSES12}
        P4 = {a: np.zeros(N_PALIERS) for a in [1, 3]}
        P3 = {a: np.zeros(N_PALIERS) for a in [1, 2]}

        for i in range(N_PALIERS):
            idx = idx_paliers[i]
            if idx < 100:
                continue
            seuil = float(X_paliers[i]) ** (1.0 / u)
            gpf_pm1_i = gpf_pm1[:idx]
            lisse_i = (gpf_pm1_i <= seuil)
            n_i = float(idx)
            P_global[i] = np.count_nonzero(lisse_i) / n_i

            c12_i = classes12[:idx]
            c4_i = classes4[:idx]
            c3_i = classes3[:idx]

            for a in CLASSES12:
                mask = (c12_i == a)
                n_a = np.count_nonzero(mask)
                if n_a > 0:
                    P12[a][i] = np.count_nonzero(lisse_i & mask) / float(n_a)

            for a in [1, 3]:
                mask = (c4_i == a)
                n_a = np.count_nonzero(mask)
                if n_a > 0:
                    P4[a][i] = np.count_nonzero(lisse_i & mask) / float(n_a)

            for a in [1, 2]:
                mask = (c3_i == a)
                n_a = np.count_nonzero(mask)
                if n_a > 0:
                    P3[a][i] = np.count_nonzero(lisse_i & mask) / float(n_a)

        dens_finale = P_global[-1]
        attendu = 0.41 if u == 2 else 0.11
        g1_ok = abs(dens_finale - attendu) < 0.08
        if not g1_ok:
            g1_all_ok = False
        print(f"  G1 densite globale finale : {dens_finale:.4f} (attendu ~{attendu}) -> {'OK' if g1_ok else 'ECHEC'}")

        alphas = []
        for a in CLASSES12:
            q4 = a % 4
            q3 = a % 3
            num = P12[a] * P_global
            den = P4[q4] * P3[q3]
            C = num / np.maximum(den, 1e-12)
            residu = C - 1.0

            # CORRECTION v2 : régression sur la sous-fenêtre [10^6, 10^8]
            valide = (np.abs(residu) > 1e-10) & (loglogX_paliers > 0) & mask_reg_window
            alpha = 0.0
            if np.sum(valide) > 20:
                coeffs = np.polyfit(loglogX_paliers[valide], np.log(np.abs(residu[valide])), 1)
                alpha = -coeffs[0]
                A = np.exp(coeffs[1])
                # Tendance appliquée à TOUTE la fenêtre
                tendance = A / (logX_paliers ** alpha)
                residu_norm = residu / np.maximum(tendance, 1e-12)
            else:
                residu_norm = residu.copy()

            alphas.append(alpha)

            r = residu_norm - np.mean(residu_norm)
            win = np.hanning(N_PALIERS)
            fft_vals = np.fft.fft(r * win)
            freqs = np.fft.fftfreq(N_PALIERS, d=ds)
            pos_mask = freqs > 0
            freqs_pos = freqs[pos_mask]
            ampl = np.abs(fft_vals[pos_mask])
            t_vals = 2 * math.pi * freqs_pos

            peaks = find_peaks(t_vals, ampl, t_min=4.0, thresh_factor=3.0)
            print(f"  Classe {a:>2}: alpha = {alpha:.3f}, pics principaux : ", end="")
            if peaks:
                print(", ".join(f"{t:.2f}" for _, t in peaks[:6]))
            else:
                print("(aucun pic net)")

            for amp, t in peaks:
                z, gap = nearest_zero(t)
                if gap < 0.60:
                    zeta_matches.append((u, a, t, z, gap))

        alpha_ok = all(1.2 <= x <= 3.0 for x in alphas)
        if not alpha_ok:
            g2_all_ok = False
        print(f"  G2 alpha dans [1.2, 3.0] -> {'OK' if alpha_ok else 'ECHEC'}")
        print()

    dt = time.time() - t0
    print("=" * 70)
    if g1_all_ok and g2_all_ok and g3_ok:
        print("VERDICT : AUDIT VERT")
    else:
        print("VERDICT : ECHEC DE GARDE")

    if zeta_matches:
        print(f"  {len(zeta_matches)} correspondances zeta (ecart < 0.60) :")
        for u, a, t, z, gap in zeta_matches:
            print(f"    u={u}, classe {a}: pic t = {t:.2f}, zeta = {z:.3f}, ecart = {gap:.2f}")
    else:
        print("  Aucune correspondance zeta nette (ecart < 0.60) detectee.")

    print(f"\nTemps total : {dt:.2f} s")
    print("[OK]")

if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    main()