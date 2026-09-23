#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# Non-commercial use only. Commercial use prohibited without written consent.
# =============================================================================
"""
injection_spectrale.py — Addendum XLI. Compagnon n.30.
Test d'injection spectrale : fermeture de la boucle des pics bas-t.

Question : les pics bas-t (4,54 ; 5,45 ; 7,26) sont-ils des artefacts/harmoniques
des zéros de χ12, ou portent-ils une structure indépendante ?

Protocole :
  1. Calcul du résidu R(X) de C1 (u=2, classe 1) sur 600 paliers [10^5, 10^8].
  2. Construction d'une base d'injection à partir des zéros de χ12 (Addendum XL) :
     γ = [3,8046 ; 6,6922 ; 8,8906 ; 11,1884].
     Base : cos(γ ln ln X) et sin(γ ln ln X).
  3. Ajustement par moindres carrés de R(X) sur cette base pour obtenir R_fit(X).
  4. Soustraction : R_clean(X) = R(X) - R_fit(X).
  5. FFT comparée de R(X) et R_clean(X) avec fenêtre de Hann.

Gardes pré-enregistrées :
  G0 (efficacité du fit) : la variance expliquée par R_fit doit être > 5%.
  G1 (nettoyage des cibles) : l'amplitude des pics FFT aux fréquences γ doit
     chuter d'au moins 50% après soustraction.
  G2 (verdict des orphelins) : si les pics orphelins (4,54 ; 5,45 ; 7,26)
     chutent aussi → artefacts. S'ils persistent → STRUCTURE.
"""
import sys
import time
import math
import numpy as np

X_MAX = 10**8
X_MIN = 10**5
N_PALIERS = 600
U = 2
CLASSE = 1

# Zéros de χ12 calculés dans l'Addendum XL
ZEROS_CHI12 = [3.8046, 6.6922, 8.8906, 11.1884]

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
    print("injection_spectrale.py — Addendum XLI : test d'injection spectrale")
    print("=" * 70)
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

    P_global = np.zeros(N_PALIERS)
    P12 = np.zeros(N_PALIERS)
    P4 = np.zeros(N_PALIERS)
    P3 = np.zeros(N_PALIERS)

    for i in range(N_PALIERS):
        idx = idx_paliers[i]
        if idx < 100:
            continue
        seuil = float(X_paliers[i]) ** (1.0 / U)
        gpf_pm1_i = gpf_pm1[:idx]
        lisse_i = (gpf_pm1_i <= seuil)
        n_i = float(idx)
        P_global[i] = np.count_nonzero(lisse_i) / n_i

        c12_i = classes12[:idx]
        c4_i = classes4[:idx]
        c3_i = classes3[:idx]

        mask12 = (c12_i == CLASSE)
        n_12 = np.count_nonzero(mask12)
        if n_12 > 0:
            P12[i] = np.count_nonzero(lisse_i & mask12) / float(n_12)

        mask4 = (c4_i == (CLASSE % 4))
        n_4 = np.count_nonzero(mask4)
        if n_4 > 0:
            P4[i] = np.count_nonzero(lisse_i & mask4) / float(n_4)

        mask3 = (c3_i == (CLASSE % 3))
        n_3 = np.count_nonzero(mask3)
        if n_3 > 0:
            P3[i] = np.count_nonzero(lisse_i & mask3) / float(n_3)

    # Calcul de C(X) et du résidu
    C = (P12 * P_global) / np.maximum(P4 * P3, 1e-12)
    residu = C - 1.0

    # Régression de tendance sur [10^6, 10^8] comme dans Addendum XXXVII
    mask_reg = (X_paliers >= 10**6)
    valide = (np.abs(residu) > 1e-10) & (loglogX_paliers > 0) & mask_reg
    alpha = 0.0
    if np.sum(valide) > 20:
        coeffs = np.polyfit(loglogX_paliers[valide], np.log(np.abs(residu[valide])), 1)
        alpha = -coeffs[0]
        A = np.exp(coeffs[1])
        tendance = A / (logX_paliers ** alpha)
        residu_norm = residu / np.maximum(tendance, 1e-12)
    else:
        residu_norm = residu.copy()

    R = residu_norm - np.mean(residu_norm)

        # --- TEST D'INJECTION v2 ---
    print("Construction de la base d'injection (zeros de chi12)...")
    # CORRECTION v2 : l'oscillation est en ln X, pas en ln ln X (formule explicite)
    M = np.zeros((N_PALIERS, 2 * len(ZEROS_CHI12)))
    for j, gamma in enumerate(ZEROS_CHI12):
        M[:, 2*j] = np.cos(gamma * logX_paliers)
        M[:, 2*j + 1] = np.sin(gamma * logX_paliers)

    # Moindres carrés : M * beta = R
    beta, residuals, rank, s = np.linalg.lstsq(M, R, rcond=None)
    R_fit = M @ beta
    R_clean = R - R_fit

    variance_R = np.var(R)
    variance_fit = np.var(R_fit)
    r2 = variance_fit / variance_R if variance_R > 0 else 0.0
    print(f"  Variance expliquee par l'injection (R2) : {r2:.4f}")
    g0_ok = r2 > 0.05
    print(f"  G0 efficacite du fit (R2 > 0.05) -> {'OK' if g0_ok else 'ECHEC'}")
    print()

    # FFT comparée
    win = np.hanning(N_PALIERS)
    fft_R = np.fft.fft(R * win)
    fft_clean = np.fft.fft(R_clean * win)
    freqs = np.fft.fftfreq(N_PALIERS, d=ds)
    pos_mask = freqs > 0
    freqs_pos = freqs[pos_mask]
    ampl_R = np.abs(fft_R[pos_mask])
    ampl_clean = np.abs(fft_clean[pos_mask])
    t_vals = 2 * math.pi * freqs_pos

    print("Analyse des pics avant et apres injection :")
    print(f"  {'Frequence':<10} | {'Amplitude Avant':<15} | {'Amplitude Apres':<15} | {'Chute %':<10} | {'Cible chi12'}")
    print("-" * 75)
    
    g1_ok = True
    orphan_persistence = []

    # Vérifier les fréquences cibles (chi12)
    for gamma in ZEROS_CHI12:
        idx = np.argmin(np.abs(t_vals - gamma))
        t_found = t_vals[idx]
        amp_before = ampl_R[idx]
        amp_after = ampl_clean[idx]
        chute = (1 - amp_after / amp_before) * 100 if amp_before > 0 else 0
        print(f"  {t_found:<10.4f} | {amp_before:<15.4f} | {amp_after:<15.4f} | {chute:>6.1f} %  | OUI")
        if chute < 50:
            g1_ok = False

    print("-" * 75)
    # Vérifier les orphelins
    orphelins = [4.54, 5.45, 7.26]
    for t_orph in orphelins:
        idx = np.argmin(np.abs(t_vals - t_orph))
        t_found = t_vals[idx]
        amp_before = ampl_R[idx]
        amp_after = ampl_clean[idx]
        chute = (1 - amp_after / amp_before) * 100 if amp_before > 0 else 0
        persiste = chute < 50
        orphan_persistence.append((t_orph, chute, persiste))
        print(f"  {t_found:<10.4f} | {amp_before:<15.4f} | {amp_after:<15.4f} | {chute:>6.1f} %  | NON (orphelin)")

    print()
    if g0_ok and g1_ok:
        print("G1 nettoyage des cibles (chute > 50%) -> OK")
    else:
        print("G1 nettoyage des cibles (chute > 50%) -> ECHEC")

    print()
    print("VERDICT SUR LES ORPHELINS :")
    tous_artefacts = all(not p[2] for p in orphan_persistence)
    tous_persistents = all(p[2] for p in orphan_persistence)
    
    if tous_artefacts:
        print("  -> Les orphelins ont chute : ils etaient des harmoniques/artefacts de chi12.")
        print("  -> STATUT : Boucle fermee. Pas de structure bas-t nouvelle.")
    elif tous_persistents:
        print("  -> Les orphelins persistent malgre le nettoyage de chi12.")
        print("  -> STATUT : STRUCTURE REELLE DETECTEE (Ouverture majeure).")
    else:
        print("  -> Resultat mixte : certains orphelins persistent, d'autres non.")
        print("  -> STATUT : STRUCTURE PARTIELLE (Ouverture a investiguer).")

    print()
    print(f"Temps total : {time.time() - t0:.2f} s")
    print("[OK]")

if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    main()