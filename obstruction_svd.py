#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# Non-commercial use only. Commercial use prohibited without written consent.
# =============================================================================
"""
obstruction_svd.py — Addendum XXXVIII. Compagnon n.27.
Le rang de l'obstruction : SVD de la matrice des marges de lissite.

Inspiration publiee : E. Tang, "A quantum-inspired classical algorithm for
recommendation systems" (STOC'19) — l'hypothese de rang faible comme structure
exploitable. Ici, on MESURE le rang de l'obstruction au lieu de le supposer.

Question : la matrice L[(M,a), u] = ln( p(a,u,M) / p_glob(u) ) est-elle dominee
par une composante de rang 1 (le diviseur force d(a) amplifie par la profondeur
u), et le residu porte-t-il une structure au-dela du bruit binomial ?

Protocole :
  - Crible GPF jusqu'a X = 10^7 (regle cumulative P+(p-1) <= X^(1/u)).
  - Modules M in {12, 24, 60} ; classes unites a mod M ; u in {2, 3, 4, 5}.
  - Matrice L (28 lignes x 4 colonnes) ; SVD ; fractions de variance.
  - Alignement du premier vecteur singulier ligne avec ln d(a).
  - Residu R = L - sigma1 u1 v1^T compare au bruit binomial attendu.

Gardes pre-enregistrees :
  G1 (densite globale) : ~0,41 en u=2, ~0,11 en u=3 (etalon maison).
  G2 (rang 1) : fraction de variance de sigma1 >= 0,90.
  G3 (alignement) : |Pearson(u1, ln d)| >= 0,95 ; Spearman par module >= 0,95.
  G4 (residu) : RMS(R)/RMS(bruit) <= 2,0 ; au-dela -> STRUCTURE (ouverture).
"""
import sys
import time
import math
import numpy as np

X_MAX = 10**7
US = [2, 3, 4, 5]
MODULES = [12, 24, 60]


def crible_premiers_gpf(n):
    gpf = np.zeros(n + 1, dtype=np.int32)
    for i in range(2, n + 1):
        if gpf[i] == 0:
            gpf[i::i] = i
    is_prime = (gpf == np.arange(n + 1, dtype=np.int32))
    is_prime[0] = False
    is_prime[1] = False
    return is_prime, gpf


def forced_valuation(a, q, k):
    """E[v_q(p-1) | p ≡ a mod q^k] : k + 1/(q-1) si a ≡ 1 mod q^k,
    sinon la valuation exacte de (a-1) mod q^k."""
    if (a - 1) % (q ** k) == 0:
        return k + 1.0 / (q - 1)
    r = (a - 1) % (q ** k)
    v = 0
    while r % q == 0:
        v += 1
        r //= q
    return float(v)


def forced_divisor(a, M):
    d = 1.0
    m = M
    q = 2
    while m > 1:
        if m % q == 0:
            k = 0
            while m % q == 0:
                m //= q
                k += 1
            d *= q ** forced_valuation(a, q, k)
        q += 1 if q == 2 else 2
    return d


def spearman(x, y):
    rx = np.argsort(np.argsort(np.asarray(x, dtype=float)))
    ry = np.argsort(np.argsort(np.asarray(y, dtype=float)))
    return float(np.corrcoef(rx, ry)[0, 1])


def pearson(x, y):
    return float(np.corrcoef(np.asarray(x, dtype=float),
                             np.asarray(y, dtype=float))[0, 1])


def rms(v):
    v = np.asarray(v, dtype=float).ravel()
    return float(np.sqrt(np.mean(v ** 2)))


def main():
    t0 = time.time()
    print("=" * 70)
    print("obstruction_svd.py — Addendum XXXVIII : le rang de l'obstruction")
    print("=" * 70)
    print()
    print(f"Crible jusqu'a {X_MAX} ...")
    t_c = time.time()
    is_prime, gpf = crible_premiers_gpf(X_MAX)
    print(f"Crible pret en {time.time() - t_c:.1f} s")

    premiers = np.nonzero(is_prime)[0]
    premiers = premiers[premiers >= 3]
    gpf_pm1 = gpf[premiers - 1]
    clsM = {M: premiers % M for M in MODULES}

    rows = [(M, a, math.log(forced_divisor(a, M)))
            for M in MODULES for a in range(1, M) if math.gcd(a, M) == 1]
    n_rows = len(rows)
    print(f"Matrice : {n_rows} lignes (classes) x {len(US)} colonnes (u)")
    print()

    L = np.zeros((n_rows, len(US)))
    Sig = np.zeros((n_rows, len(US)))
    g1_ok = {}
    for j, u in enumerate(US):
        seuil = float(X_MAX) ** (1.0 / u)
        lisse = (gpf_pm1 <= seuil)
        glob = float(lisse.mean())
        if u == 2:
            ok = 0.33 <= glob <= 0.49
            g1_ok[2] = ok
            print(f"  G1 densite globale u=2 : {glob:.4f} -> {'OK' if ok else 'ECHEC'}")
        if u == 3:
            ok = 0.06 <= glob <= 0.16
            g1_ok[3] = ok
            print(f"  G1 densite globale u=3 : {glob:.4f} -> {'OK' if ok else 'ECHEC'}")
        for i, (M, a, _) in enumerate(rows):
            mask = (clsM[M] == a)
            n_a = int(mask.sum())
            c = int((lisse & mask).sum())
            if c == 0:
                c = 0.5
                print(f"  NOTE : cellule vide (M={M}, a={a}, u={u}), demi-comptage")
            p = c / float(n_a)
            L[i, j] = math.log(p / glob)
            Sig[i, j] = math.sqrt((1.0 - p) / (p * float(n_a)))

    print()
    U, s, Vt = np.linalg.svd(L, full_matrices=False)
    frac = (s ** 2) / float(np.sum(s ** 2))
    print("Valeurs singulieres et fractions de variance :")
    for idx in range(len(s)):
        print(f"  sigma{idx+1} = {s[idx]:9.4f}   fraction = {frac[idx]:.4f}")
    g2_ok = frac[0] >= 0.90
    print(f"  G2 fraction rang 1 >= 0,90 : {frac[0]:.4f} -> {'OK' if g2_ok else 'ECHEC'}")
    print()

    g = np.array([r[2] for r in rows])
    u1 = U[:, 0]
    corr = pearson(u1, g)
    signe = 1.0 if corr >= 0 else -1.0
    u1 = u1 * signe
    kappa = s[0] * Vt[0, :] * signe
    kappa_n = kappa / kappa[0]
    print("Amplification kappa(u) normalisee (u=2 -> 1) : " +
          " ; ".join(f"u={u}: {k:.3f}" for u, k in zip(US, kappa_n)))
    g3_ok = abs(corr) >= 0.95
    print(f"Alignement u1 vs ln d : Pearson = {corr:+.4f} -> {'OK' if abs(corr) >= 0.95 else 'ECHEC'}")
    sp_ok = True
    for M in MODULES:
        idx = [i for i, r in enumerate(rows) if r[0] == M]
        sp = spearman(L[idx, 0], g[idx])
        if sp < 0.95:
            sp_ok = False
        print(f"  Spearman module {M:>2} (u=2 vs ln d) : {sp:.4f}")
    g3_ok = g3_ok and sp_ok
    print(f"  G3 alignement -> {'OK' if g3_ok else 'ECHEC'}")
    print()

    R = L - np.outer(s[0] * U[:, 0], Vt[0, :])
    ratio = rms(R) / rms(Sig)
    g4_ok = ratio <= 2.0
    print(f"Residu apres rang 1 : RMS(R) = {rms(R):.4f}, RMS(bruit) = {rms(Sig):.4f}")
    print(f"  G4 ratio residu/bruit = {ratio:.2f} -> {'OK (bruit)' if g4_ok else 'STRUCTURE (ouverture)'}")

    fam = {}
    for i, (M, a, ld) in enumerate(rows):
        fam.setdefault((M, round(math.exp(ld), 9)), []).append(i)
    jumeaux = [v for v in fam.values() if len(v) > 1]
    if jumeaux:
        within = rms([R[i, j] for v in jumeaux for i in v for j in range(len(US))])
        noise = rms([Sig[i, j] for v in jumeaux for i in v for j in range(len(US))])
        print(f"  Familles jumelles : {len(jumeaux)} ; RMS residu intra = {within:.4f} vs bruit {noise:.4f}")
    print()

    if g1_ok.get(2, False) and g1_ok.get(3, False) and g2_ok and g3_ok:
        print("VERDICT : AUDIT VERT")
        if not g4_ok:
            print("  Ouverture mesuree : structure au-dela du rang 1 (residu > bruit).")
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