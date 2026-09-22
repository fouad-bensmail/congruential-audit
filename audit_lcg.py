#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# =============================================================================
"""
audit_lcg.py v3 — Axe 2 de l'anti-fraude : audit des generateurs congruentiels.
Addendum XXXV. Compagnon n.24.

Refus publies :
  v1 : graine de RANDU paire (42424242) avec module 2^31 — la suite reste paire,
       RANDU produit 0 premiers, et le verdict AUDIT VERT a masque ce silence.
  v2 : graines impaires + diagnostic de parite, mais le calcul s'arretait apres
       le DRAPEAU de parite sans chiffrer le biais de lissite.
Corrections du forgeron :
  (1) graines impaires pour les LCG a module puissance de 2 ;
  (2) garde d'echantillon : un generateur produisant < 100 premiers declenche
      un DRAPEAU (au lieu d'un silence) ;
  (3) diagnostic de parite : detection des suites confinees a une parite ;
  (4) NOUVEAU v3 : le z-score de lissite est calcule MEME pour les generateurs
      a parite anormale, afin de capturer les deux signatures (parite + lissite).
"""
import sys
import time
import math
import secrets
import numpy as np

X_MAX = 10**6
N_CANDIDATS = 150000
U = 2
SEUIL_ECHANTILLON = 100

def crible_premiers_gpf(n):
    gpf = np.zeros(n + 1, dtype=np.int32)
    for i in range(2, n + 1):
        if gpf[i] == 0:
            gpf[i::i] = i
    is_prime = (gpf == np.arange(n + 1, dtype=np.int32))
    is_prime[0] = False
    is_prime[1] = False
    return is_prime, gpf

def gen_REF(n, x_max):
    return np.array([secrets.randbelow(x_max) for _ in range(n)], dtype=np.int64)

def gen_LCG(n, x_max, a, c, m, seed):
    x = seed
    vals = np.empty(n, dtype=np.int64)
    for i in range(n):
        x = (a * x + c) % m
        vals[i] = x % x_max
    return vals

def audit(vals, is_prime, gpf):
    mask = is_prime[vals]
    premiers = vals[mask]
    premiers = premiers[premiers >= 3]
    n_p = len(premiers)
    prop_paires = float(np.mean(vals % 2 == 0))
    if n_p == 0:
        return 0, 0.0, {}, prop_paires
    pm1 = premiers - 1
    seuils = (pm1 ** (1.0 / U)).astype(np.int64)
    lisse = gpf[pm1] <= seuils
    prop = float(np.mean(lisse))
    par_classe = {}
    c12 = premiers % 12
    for a in [1, 5, 7, 11]:
        m_a = (c12 == a)
        n_a = int(np.sum(m_a))
        prop_a = float(np.mean(lisse[m_a])) if n_a > 0 else 0.0
        par_classe[a] = (n_a, prop_a)
    return n_p, prop, par_classe, prop_paires

def main():
    t0 = time.time()
    print("=" * 70)
    print("audit_lcg.py v3 — Axe 2 de l'anti-fraude : audit des generateurs congruentiels")
    print("=" * 70)
    print()
    print(f"Crible jusqu'a {X_MAX} ...")
    t_c = time.time()
    is_prime, gpf = crible_premiers_gpf(X_MAX)
    print(f"Crible pret en {time.time()-t_c:.1f} s")
    print()

    generators = [
        ("REF    (alea veritable)", lambda: gen_REF(N_CANDIDATS, X_MAX)),
        ("GLIBC  (glibc rand)"   , lambda: gen_LCG(N_CANDIDATS, X_MAX, 1103515245, 12345, 2**31, 123456789)),
        ("MINSTD (Park-Miller)"  , lambda: gen_LCG(N_CANDIDATS, X_MAX, 16807, 0, 2**31 - 1, 987654321)),
        ("RANDU  (historique)"   , lambda: gen_LCG(N_CANDIDATS, X_MAX, 65539, 0, 2**31, 42424243)),
    ]

    results = {}
    print(f"{'Generateur':<24} {'Premiers':>9} {'Prop p-1 lisse':>15} {'Prop pairs':>11}")
    print("-" * 62)
    for name, gen_fn in generators:
        vals = gen_fn()
        n_p, prop, par_classe, prop_paires = audit(vals, is_prime, gpf)
        results[name] = (n_p, prop, par_classe, prop_paires)
        print(f"{name:<24} {n_p:>9} {prop:>15.4f} {prop_paires:>11.4f}")
    print()

    n_ref, p_ref, pc_ref, _ = results["REF    (alea veritable)"]
    print("--- Gardes ---")
    g1_ok = 0.30 <= p_ref <= 0.55
    print(f"  G1 (reference saine, prop dans [0.30, 0.55]) : {'OK' if g1_ok else 'ECHEC'} (prop = {p_ref:.4f}, n = {n_ref})")
    print(f"  Reference par classe mod 12 :")
    for a in [1, 5, 7, 11]:
        n_a, prop_a = pc_ref.get(a, (0, 0.0))
        print(f"      c{a:<3}: n = {n_a:>5}, prop = {prop_a:.4f}")
    print()

    print("--- Scores de fraude (ecart en sigmas contre REF) ---")
    all_conformes = True
    drapeaux = []
    for name, (n_g, p_g, _, prop_paires) in results.items():
        if name.startswith("REF"):
            continue
        if n_g < SEUIL_ECHANTILLON:
            all_conformes = False
            drapeaux.append((name, n_g, prop_paires, None))
            print(f"  {name:<24}: n = {n_g} < {SEUIL_ECHANTILLON} -> DRAPEAU (echantillon insuffisant)")
            continue
        signale = False
        motifs = []
        if prop_paires > 0.99 or prop_paires < 0.01:
            signale = True
            motifs.append(f"suite confinee a une parite (prop pairs = {prop_paires:.3f})")
        se = math.sqrt(p_ref*(1-p_ref)/n_ref + p_g*(1-p_g)/n_g)
        z = (p_g - p_ref) / se if se > 0 else 0.0
        if abs(z) >= 3:
            signale = True
            motifs.append(f"biais de lissite (z = {z:+.2f} sigma)")
        verdict = "DRAPEAU" if signale else "CONFORME"
        print(f"  {name:<24}: prop lisse = {p_g:.4f}, z = {z:+.2f} sigma, prop pairs = {prop_paires:.3f} -> {verdict}")
        if motifs:
            print(f"      motifs : {' ; '.join(motifs)}")
        if signale:
            all_conformes = False
            drapeaux.append((name, n_g, prop_paires, z))
    print()

    dt = time.time() - t0
    if g1_ok and all_conformes:
        print("VERDICT : AUDIT VERT")
        print("  La reference est saine ; aucun biais de lissite detectable sur les LCG")
        print("  audites contre l'alea veritable a cette echelle.")
    elif g1_ok and not all_conformes:
        print("VERDICT : DRAPEAU (au moins un generateur signale)")
        for name, n_g, pp, z in drapeaux:
            zs = f"z = {z:+.2f} sigma" if z is not None else "z non calcule"
            print(f"  {name}: n = {n_g}, prop pairs = {pp:.3f}, lissite {zs}")
    else:
        print("VERDICT : ECHEC DE GARDE (reference hors norme)")
    print(f"\nTemps total : {dt:.2f} s")
    print("[OK]")

if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    main()