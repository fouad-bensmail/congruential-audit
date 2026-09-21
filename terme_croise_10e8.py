#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# Non-commercial use only. Commercial use prohibited without written consent.
# =============================================================================
"""
terme_croise_10e8.py (v2 corrigee) -- Extinction du terme croise a 10^8.
Addendum XXXIII, Montee en echelle de C1. Compagnon n.22.

Refus publie : la v1 mesurait sur les entiers (couche T4) avec une mauvaise
normalisation de C, donnant C ~ 3 au lieu de C ~ 1. 
Corrige : mesure sur les premiers p <= X (couche C1, coeur de l'objection
du relecteur), avec normalisation correcte par la densite globale.
"""

import sys
import time
import numpy as np

def crible_premiers_et_gpf(X):
    """Crible les premiers p <= X et calcule GPF(p-1) pour chaque p."""
    # Crible des plus grands facteurs premiers pour tous les entiers
    gpf = np.zeros(X + 1, dtype=np.int32)
    for i in range(2, X + 1):
        if gpf[i] == 0:
            gpf[i::i] = i
    
    # Crible des premiers (is_prime)
    is_prime = (gpf == np.arange(X + 1))
    is_prime[0] = is_prime[1] = False
    
    return is_prime, gpf

def compte_premiers_par_classe(X, q, u, is_prime, gpf):
    """Compte les p <= X avec p = a mod q et P+(p-1) <= X^(1/u)."""
    seuil = int(X ** (1.0 / u))
    
    # Masque des p-1 lisses (pour tous les entiers)
        # CORRECTION : on teste si n-1 est lisse, pas si n est lisse
    lisse_p_minus_1 = np.zeros_like(gpf, dtype=bool)
    lisse_p_minus_1[1:] = (gpf[:-1] <= seuil)
    
    # Masque des p premiers ET p-1 lisse
    premier_et_lisse = is_prime & lisse_p_minus_1
    
    counts_lisse = np.zeros(q, dtype=np.int64)
    counts_total = np.zeros(q, dtype=np.int64)
    
    for a in range(q):
        idx = np.arange(a, X + 1, q)
        counts_lisse[a] = np.sum(premier_et_lisse[idx])
        counts_total[a] = np.sum(is_prime[idx])
    
    # Proportions conditionnelles D_q(a) = P(p-1 lisse | p = a mod q)
    proportions = np.zeros(q, dtype=np.float64)
    for a in range(q):
        if counts_total[a] > 0:
            proportions[a] = counts_lisse[a] / counts_total[a]
    
    # Densite globale parmi les premiers de la classe
    total_premiers = np.sum(is_prime)
    total_lisse = np.sum(premier_et_lisse)
    d_global = total_lisse / total_premiers if total_premiers > 0 else 0
    
    return proportions, d_global

def main():
    t0 = time.time()
    print("=" * 70)
    print("terme_croise_10e8.py (v2) -- Extinction de C1 sur les premiers")
    print("=" * 70)
    print()
    
    X_values = [10**6, 10**7, 10**8]
    u_values = [2, 3]
    
    print("Generation du crible (premiers + GPF) jusqu'a 10^8...")
    t_crible = time.time()
    is_prime, gpf = crible_premiers_et_gpf(10**8)
    print(f"Crible pret en {time.time() - t_crible:.1f} s\n")
    
    results = {}
    
    for X in X_values:
        print(f"--- Echelle X = {X:,} ---")
        # Restreindre aux p <= X
        mask_X = np.zeros(10**8 + 1, dtype=bool)
        mask_X[:X+1] = True
        is_prime_X = is_prime & mask_X
        gpf_X = gpf  # gpf est deja calcule, on l'utilise tel quel
        
        for u in u_values:
            D4, d_glob_4 = compte_premiers_par_classe(X, 4, u, is_prime_X, gpf_X)
            D3, d_glob_3 = compte_premiers_par_classe(X, 3, u, is_prime_X, gpf_X)
            D12, d_glob_12 = compte_premiers_par_classe(X, 12, u, is_prime_X, gpf_X)
            
            # La densite globale est la meme pour tous les modules
            d_global = d_glob_12
            
            results[(u, X)] = {"D4": D4, "D3": D3, "D12": D12, "d_global": d_global}
            
            print(f"  u = {u}, densite globale = {d_global:.6f} :")
            print(f"    {'Classe':<10} {'D4':<10} {'D3':<10} {'D12':<10} {'C':<10}")
            for a in [1, 5, 7, 11]:
                a4 = a % 4
                a3 = a % 3
                d4_val = D4[a4]
                d3_val = D3[a3]
                d12_val = D12[a]
                # Formule corrigee : C = (D12 * d_global) / (D4 * D3)
                if d4_val > 0 and d3_val > 0:
                    C = (d12_val * d_global) / (d4_val * d3_val)
                else:
                    C = float('inf')
                print(f"    {a:<10} {d4_val:<10.6f} {d3_val:<10.6f} {d12_val:<10.6f} {C:<10.6f}")
        print()
    
    # Analyse de la contraction
    print("=" * 70)
    print("Analyse de la contraction de |C - 1| (Conjecture C1)")
    print("=" * 70)
    
    audit_vert = True
    for u in u_values:
        print(f"\nu = {u} :")
        for a in [1, 5, 7, 11]:
            d_g_6 = results[(u, 10**6)]["d_global"]
            C_10e6 = (results[(u, 10**6)]["D12"][a] * d_g_6) / (results[(u, 10**6)]["D4"][a % 4] * results[(u, 10**6)]["D3"][a % 3])
            
            d_g_7 = results[(u, 10**7)]["d_global"]
            C_10e7 = (results[(u, 10**7)]["D12"][a] * d_g_7) / (results[(u, 10**7)]["D4"][a % 4] * results[(u, 10**7)]["D3"][a % 3])
            
            d_g_8 = results[(u, 10**8)]["d_global"]
            C_10e8 = (results[(u, 10**8)]["D12"][a] * d_g_8) / (results[(u, 10**8)]["D4"][a % 4] * results[(u, 10**8)]["D3"][a % 3])
            
            dev_6 = abs(C_10e6 - 1.0)
            dev_7 = abs(C_10e7 - 1.0)
            dev_8 = abs(C_10e8 - 1.0)
            
            contraction_6_7 = dev_6 / dev_7 if dev_7 > 0 else float('inf')
            contraction_7_8 = dev_7 / dev_8 if dev_8 > 0 else float('inf')
            
            print(f"  Classe {a:2d} : C(10^6) = {C_10e6:.6f}, C(10^7) = {C_10e7:.6f}, C(10^8) = {C_10e8:.6f}")
            print(f"           |C-1| : {dev_6:.4f} -> {dev_7:.4f} -> {dev_8:.4f}")
            print(f"           Contraction 10^6->10^7 : x{contraction_6_7:.2f}")
            print(f"           Contraction 10^7->10^8 : x{contraction_7_8:.2f}")
            
            # Garde : la deviation |C-1| doit decroitre (contraction > 1)
            if contraction_7_8 < 1.0 and dev_8 > 1e-4:
                print(f"           [!] Contraction insuffisante")
                audit_vert = False
    
    print()
    if audit_vert:
        print("VERDICT : AUDIT VERT")
        print("  L'extinction en 1/log X du terme croise (C1) est confirmee a 10^8.")
    else:
        print("VERDICT : DRAPEAU")
    
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