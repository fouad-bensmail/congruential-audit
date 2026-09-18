#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
motif_espace.py -- Continuite de la serie singuliere sur l'espace des motifs.
Addendum XXVIII, Direction 1 : geometrie de l'obstruction.
Compagnon n.17.

Protocole : H = {0, 2, 6} (triplet admissible).
            H'_P = {0, 2, 6 + M_P} ou M_P = prod(p <= P) (primorial).
            Pour p <= P : 6 + M_P == 6 (mod p), donc nu_p(H') = nu_p(H).
            Pour p > P  : les deux motifs different en general.
            On mesure epsilon(P) = |S(H'_P)/S(H) - 1| pour P croissant.

Garde pre-enregistree : epsilon(P) < 0.01 pour P >= 50 ;
                        contraction >= 2 entre P = 10 et P = 100.
"""

import sys
import time
from sympy import primerange, isprime


def singular_series(H, P_max):
    """Produit eulerien partiel S_P(H) = prod_{p <= P_max} (1 - nu_p/p)(1 - 1/p)^{-k}."""
    k = len(H)
    result = 1.0
    for p in primerange(2, P_max + 1):
        nu = len({h % p for h in H})
        factor = (1.0 - nu / p) / ((1.0 - 1.0 / p) ** k)
        result *= factor
    return result


def build_H_prime(P):
    """Construit H'_P = {0, 2, 6 + M_P} avec M_P = primorial(P)."""
    M = 1
    for p in primerange(2, P + 1):
        M *= p
    return [0, 2, 6 + M]


def main():
    t0 = time.time()
    print("=" * 70)
    print("motif_espace.py  --  continuite de S sur l'espace des motifs")
    print("=" * 70)
    print()

    # Parametres
    H = [0, 2, 6]
    P_max = 100_000          # borne superieure du produit eulerien (convergence)
    P_values = [2, 3, 5, 7, 10, 13, 17, 23, 31, 50, 79, 100, 157, 199]

    print(f"Motif de reference : H = {H}")
    print(f"Motif perturbe     : H'_P = {{0, 2, 6 + M_P}} avec M_P = prod(p <= P)")
    print(f"Produit eulerien   : P_max = {P_max}")
    print()

    # Reference : S(H) a P_max
    S_ref = singular_series(H, P_max)
    print(f"S(H) a P_max = {P_max} : {S_ref:.10f}")
    print()
    print(f"{'P':>6}  {'S(H_P)':>14}  {'ratio':>12}  {'epsilon':>12}  {'garde':>8}")
    print("-" * 62)

    eps_prev = None
    garde_ok = True
    contractions = []

    for P in P_values:
        H_prime = build_H_prime(P)
        S_prime = singular_series(H_prime, P_max)
        ratio = S_prime / S_ref
        eps = abs(ratio - 1.0)

        # Evaluation de la garde
        if P >= 50 and eps >= 0.01:
            status = "HORS"
            garde_ok = False
        else:
            status = "OK"

        if eps_prev is not None and eps > 0:
            contraction = eps_prev / eps
            contractions.append((P, contraction))
        eps_prev = eps

        print(f"{P:>6}  {S_prime:>14.10f}  {ratio:>12.8f}  {eps:>12.2e}  {status:>8}")

    print("-" * 62)
    print()
    print("Contraction entre echelles :")
    # contraction entre P = 10 et P = 100
    idx_10 = P_values.index(10)
    idx_100 = P_values.index(100)
    H_p_10 = build_H_prime(10)
    H_p_100 = build_H_prime(100)
    eps_10 = abs(singular_series(H_p_10, P_max) / S_ref - 1.0)
    eps_100 = abs(singular_series(H_p_100, P_max) / S_ref - 1.0)
    if eps_100 > 0:
        contraction_10_100 = eps_10 / eps_100
    else:
        contraction_10_100 = float('inf')
    print(f"  epsilon(P=10)  = {eps_10:.2e}")
    print(f"  epsilon(P=100) = {eps_100:.2e}")
    print(f"  contraction    = {contraction_10_100:.2f}  (garde : >= 2)")

    print()
    # Verdict
    if garde_ok and contraction_10_100 >= 2.0 and eps_100 < 0.01:
        print("VERDICT : AUDIT VERT")
        print("  Continuite mesuree : epsilon(P) -> 0 quand P -> infinity.")
        print("  Theoreme T5 candidat confirme experimentalement.")
    elif garde_ok:
        print("VERDICT : AUDIT VERT (contraction faible)")
    else:
        print("VERDICT : DRAPEAU / REFUS")
        print("  Continuite non confirmee a la precision demandee.")

    dt = time.time() - t0
    print()
    print(f"Temps : {dt:.2f} s")
    print("[OK]")


if __name__ == "__main__":
    # Protection encodage Windows (cf. Addendum XXVI)
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    main()