#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# =============================================================================
"""
zeros_dirichlet.py v3 — Addendum XL. Compagnon n.29.
Les zeros bas-t : identification des pics bas de l'Addendum XXXVII.

Refus publies :
  v1 : crash (cmath.gamma n'existe pas).
  v2 : signe de l'integrale de la queue Euler-Maclaurin. L'integrale
       int_K^infty (r+xq)^{-s} dx converge pour Re(s)=1/2 et vaut
       u^{1-s} / (q(s-1)). Il n'y a pas de bord en M a soustraire.
       La v2 passait sign_int=-1 pour les caracteres non triviaux,
       ajoutant un terme parasite qui brisait l'equation fonctionnelle
       (G1 echouait a 1.79e-3, Z(t) complexe) et decalait les zeros
       (G2 echouait a 2/5).
  v3 : signe +1 partout. L'equation fonctionnelle est restauree.

Methode : L(1/2+it, chi) = somme directe n <= N0 + queues Euler-Maclaurin
par classe r mod q (10 termes de Bernoulli). Z(t) = exp(i theta(t)) L, reel ;
zeros par changements de signe + bissection. Garde G0 : le premier zero de
zeta doit sortir a 14,134725 +/- 0,002.

Gardes pre-enregistrees :
  G0 (methode)  : premier zero de zeta = 14,134725 +/- 0,002.
  G1 (realite)  : max|Im Z| / max|Re Z| < 1e-6 sur la grille.
  G2 (identif.) : >= 3 des 5 pics bas-t de l'Addendum XXXVII
                  (4,54 ; 5,45 ; 7,26 ; 9,08 ; 10,90) a < 0,45 d'un zero
                  calcule de chi3, chi4 ou chi12.
"""
import sys
import time
import math
import cmath
import numpy as np

N0 = 200000
M_EM = 10
T_MIN, T_MAX, T_PAS = 0.5, 15.0, 0.01
PICS_XXXVII = [4.54, 5.45, 7.26, 9.08, 10.90]

BERN = [1/6, -1/30, 1/42, -1/30, 5/66, -691/2730, 7/6,
        -3617/510, 43867/798, -174611/330, 854513/138]
FACT = [math.factorial(2 * j + 2) for j in range(len(BERN))]

_LG = [0.99999999999980993, 676.5203681218851, -1259.1392167224028,
       771.32342877765313, -176.61502916214059, 12.507343278686905,
       -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7]


def log_gamma_c(z):
    s = 0j
    while z.real < 1.5:
        s -= cmath.log(z)
        z += 1.0
    w = z - 1.0
    x = _LG[0]
    for i in range(1, 9):
        x += _LG[i] / (w + i)
    t = w + 7.5
    return s + 0.5 * math.log(2 * math.pi) + (w + 0.5) * cmath.log(t) - t + cmath.log(x)


def arg_gamma(z):
    return log_gamma_c(z).imag


def chi_trivial(n):
    return 1


def chi3(n):
    r = n % 3
    return 0 if r == 0 else (1 if r == 1 else -1)


def chi4(n):
    r = n % 4
    return 0 if r % 2 == 0 else (1 if r == 1 else -1)


def chi12(n):
    return chi4(n) * chi3(n)


CARACTERES = [("zeta", 1, chi_trivial), ("chi3", 3, chi3),
              ("chi4", 4, chi4), ("chi12", 12, chi12)]


def em_tail(r, q, s, K, m=M_EM):
    """Sum_{k>=K} (r+kq)^{-s} par Euler-Maclaurin.
    L'integrale int_K^infty (r+xq)^{-s} dx vaut u^{1-s} / (q(s-1))."""
    u = complex(r + K * q)
    ln_u = cmath.log(u)
    base = cmath.exp(-s * ln_u)
    total = cmath.exp((1.0 - s) * ln_u) / (q * (s - 1.0))
    total += 0.5 * base
    rise = 1.0 + 0j
    for n in range(1, 2 * m):
        rise *= (s + (n - 1))
        cur = base * rise * ((-1) ** n) * (q ** n) / cmath.exp(n * ln_u)
        if n % 2 == 1:
            j = (n + 1) // 2
            total -= (BERN[j - 1] / FACT[j - 1]) * cur
    return total


def precompute(chi):
    n = np.arange(1, N0 + 1, dtype=np.int64)
    a = np.array([chi(int(v)) for v in n], dtype=np.float64)
    m = a != 0
    return n[m].astype(np.float64), a[m]


def L_crit(t, q, chi, nz, az):
    s = 0.5 + 1j * t
    val = complex(np.sum(az * np.exp(-s * np.log(nz))))
    if q == 1:
        val += em_tail(0, 1, s, N0 + 1)
    else:
        for r in range(1, q + 1):
            c = chi(r)
            if c == 0:
                continue
            K = (N0 + 1 - r + q - 1) // q
            val += c * em_tail(r, q, s, K)
    return val


def Z_crit(t, q, chi, a_par, nz, az):
    Lv = L_crit(t, q, chi, nz, az)
    if q == 1:
        theta = arg_gamma(0.25 + 0.5j * t) - (t / 2.0) * math.log(math.pi)
    else:
        theta = (t / 2.0) * math.log(q / math.pi) + arg_gamma((a_par + 0.5 + 1j * t) / 2.0)
    return cmath.exp(1j * theta) * Lv


def parite(chi, q):
    return 0 if chi(q - 1) == 1 else 1


def zeros_sur_grille(q, chi, a_par, nz, az):
    ts = np.arange(T_MIN, T_MAX, T_PAS)
    Zs = np.array([Z_crit(float(t), q, chi, a_par, nz, az) for t in ts])
    imag_rel = float(np.max(np.abs(Zs.imag)) / max(np.max(np.abs(Zs.real)), 1e-30))
    z = []
    for i in range(len(ts) - 1):
        if Zs[i].real * Zs[i + 1].real < 0:
            lo, hi = float(ts[i]), float(ts[i + 1])
            flo = Zs[i].real
            for _ in range(50):
                mid = 0.5 * (lo + hi)
                fm = Z_crit(mid, q, chi, a_par, nz, az).real
                if flo * fm <= 0:
                    hi = mid
                else:
                    lo, flo = mid, fm
            z.append(0.5 * (lo + hi))
    return z, imag_rel


def main():
    t0 = time.time()
    print("=" * 70)
    print("zeros_dirichlet.py v3 — Addendum XL : les zeros bas-t")
    print("=" * 70)
    print()
    tous = {}
    imag_max = 0.0
    for nom, q, chi in CARACTERES:
        nz, az = precompute(chi)
        a_par = parite(chi, q)
        z, ir = zeros_sur_grille(q, chi, a_par, nz, az)
        tous[nom] = z
        imag_max = max(imag_max, ir)
        print(f"{nom:>6} : zeros t = " + ", ".join(f"{v:.4f}" for v in z[:8]))
    print()
    z_zeta = tous["zeta"]
    g0 = bool(z_zeta) and abs(z_zeta[0] - 14.134725) <= 0.002
    print(f"G0 premier zero de zeta : {z_zeta[0]:.6f} (attendu 14.134725 +/- 0,002) -> {'OK' if g0 else 'ECHEC'}")
    g1 = imag_max < 1e-6
    print(f"G1 realite de Z : max|Im Z|/max|Re Z| = {imag_max:.2e} -> {'OK' if g1 else 'ECHEC'}")
    print()
    cand = [(nom, v) for nom in ("chi3", "chi4", "chi12") for v in tous[nom]]
    n_match = 0
    print("Identification des pics bas-t de l'Addendum XXXVII :")
    for p in PICS_XXXVII:
        best = min(cand, key=lambda cv: abs(p - cv[1]))
        gap = abs(p - best[1])
        ok = gap < 0.45
        if ok:
            n_match += 1
        print(f"  pic {p:5.2f} -> {best[0]} t = {best[1]:.4f}, ecart = {gap:.3f} -> {'SIGNAL' if ok else 'non'}")
    g2 = n_match >= 3
    print(f"G2 identifications >= 3 sur 5 : {n_match} -> {'OK' if g2 else 'ECHEC'}")
    print()
    if g0 and g1:
        print("VERDICT : AUDIT VERT")
        if not g2:
            print("  Ouverture mesuree : les pics bas-t ne s'alignent pas sur chi3/chi4/chi12.")
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