#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# Non-commercial use only. Commercial use prohibited without written consent.
# =============================================================================
"""
synthese_diviseur_force.py -- Taxonomie universelle de l'obstruction.
Addendum XXX, Rang 3 du Programme de la Forge. Compagnon n.19.

Protocole : Unifie les cartographies mod 12, 24, 60 sous la loi unique du 
diviseur force d(a). Mesure la correlation de Spearman et l'indiscernabilite 
des familles jumelles.
Echelle : X = 10^5, u = 2.
"""

import sys
import math
import time

def gpf_sieve(n):
    """Crible pour trouver le Plus Grand Facteur Premier (GPF) jusqu'a n."""
    gpf = [0] * (n + 1)
    for i in range(2, n + 1):
        if gpf[i] == 0:  # i est premier
            for j in range(i, n + 1, i):
                gpf[j] = i
    return gpf

def get_forced_divisor(a, M):
    """Calcule le diviseur force d(a) pour la classe a mod M."""
    d_log = 0.0
    m_temp = M
    for q in range(2, M + 1):
        if m_temp % q == 0:
            # Verifie si q est premier (si m_temp % q == 0 et q n'a pas ete divise avant)
            is_prime = True
            for i in range(2, int(math.isqrt(q)) + 1):
                if q % i == 0:
                    is_prime = False
                    break
            if not is_prime:
                continue
                
            k = 0
            while m_temp % q == 0:
                k += 1
                m_temp //= q
            
                       # Valuation de (a-1) par rapport a q
            # CORRECTION : si a=1 (ou a-1 multiple de q^k), le volume est maximal
            if (a - 1) % (q**k) == 0:
                E_vq = k + 1.0 / (q - 1)
            else:
                v = 0
                val = a - 1
                while val % q == 0 and val > 0:
                    v += 1
                    val //= q
                E_vq = float(v)
                
            d_log += E_vq * math.log(q)
    return math.exp(d_log)

def rankdata(arr):
    """Calcule les rangs (avec moyennes pour les ex aequo)."""
    sorted_arr = sorted((val, idx) for idx, val in enumerate(arr))
    ranks = [0.0] * len(arr)
    i = 0
    while i < len(sorted_arr):
        j = i
        while j < len(sorted_arr) and sorted_arr[j][0] == sorted_arr[i][0]:
            j += 1
        avg_rank = (i + j + 1) / 2.0  # Rang moyen 1-based
        for k in range(i, j):
            ranks[sorted_arr[k][1]] = avg_rank
        i = j
    return ranks

def pearson(x, y):
    """Correlation de Pearson."""
    n = len(x)
    if n == 0: return 0.0
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    std_x = math.sqrt(sum((xi - mean_x)**2 for xi in x))
    std_y = math.sqrt(sum((yi - mean_y)**2 for yi in y))
    if std_x == 0 or std_y == 0: return 0.0
    return cov / (std_x * std_y)

def spearman(x, y):
    """Correlation de rang de Spearman."""
    return pearson(rankdata(x), rankdata(y))

def main():
    t0 = time.time()
    print("=" * 70)
    print("synthese_diviseur_force.py -- Taxonomie universelle (Rang 3)")
    print("=" * 70)
    
    X = 5_000_000
    u = 2
    print(f"Echelle : X = {X}, u = {u} (lissite P+(m) <= m^(1/{u}))")
    print("Generation du crible des plus grands facteurs premiers...")
    gpf = gpf_sieve(X)
    is_prime = [gpf[i] == i for i in range(X + 1)]
    is_prime[0] = is_prime[1] = False
    print("Crible pret.\n")
    
    modules = [12, 24, 60]
    global_audit_vert = True
    
    for M in modules:
        print(f"--- MODULE M = {M} ---")
        classes = [a for a in range(1, M) if math.gcd(a, M) == 1]
        
        theorical_d = []
        empirical_smoothness = []
        counts = {a: {"total": 0, "smooth": 0} for a in classes}
        
        for p in range(2, X + 1):
            if is_prime[p]:
                a = p % M
                if math.gcd(a, M) == 1:
                    counts[a]["total"] += 1
                    if gpf[p - 1] <= (p - 1)**(1/u):
                        counts[a]["smooth"] += 1
                        
        for a in classes:
            theorical_d.append(get_forced_divisor(a, M))
            rate = counts[a]["smooth"] / counts[a]["total"] if counts[a]["total"] > 0 else 0
            empirical_smoothness.append(rate)
            
        rho = spearman(theorical_d, empirical_smoothness)
        
        # Analyse des familles jumelles (variance intra vs inter)
        # Regroupe par d(a) arrondi a 1e-9
        families = {}
        for d_val, rate in zip(theorical_d, empirical_smoothness):
            key = round(d_val, 9)
            if key not in families:
                families[key] = []
            families[key].append(rate)
            
        intra_var = 0.0
        intra_count = 0
        for fam_rates in families.values():
            if len(fam_rates) > 1:
                mean_fam = sum(fam_rates) / len(fam_rates)
                intra_var += sum((r - mean_fam)**2 for r in fam_rates)
                intra_count += len(fam_rates)
        intra_var = intra_var / intra_count if intra_count > 0 else 0
        
        global_mean = sum(empirical_smoothness) / len(empirical_smoothness)
        inter_var = sum((r - global_mean)**2 for r in empirical_smoothness) / len(empirical_smoothness)
        
        ratio_var = inter_var / intra_var if intra_var > 0 else float('inf')
        
        print(f"  Classes coprimes : {len(classes)}")
        print(f"  Familles jumelles : {len(families)}")
        print(f"  Spearman (theorique vs empirique) : {rho:.4f}  (Garde : > 0.95)")
        print(f"  Ratio Variance Inter/Intra : {ratio_var:.2f}  (Garde : > 10)")
        
        if rho > 0.95 and ratio_var > 10:
            print("  Statut : OK")
        else:
            print("  Statut : ECART")
            global_audit_vert = False
        print()

    print("-" * 70)
    if global_audit_vert:
        print("VERDICT : AUDIT VERT")
        print("  La taxonomie universelle est confirmee.")
        print("  L'obstruction n'est qu'une projection du diviseur force.")
    else:
        print("VERDICT : DRAPEAU")
        
    dt = time.time() - t0
    print(f"\nTemps : {dt:.2f} s")
    print("[OK]")

if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    main()