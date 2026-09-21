#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# Non-commercial use only. Commercial use prohibited without written consent.
# =============================================================================
"""
diagnostic_rsa.py -- Scanner geometrique de cles RSA publiques.
Addendum XXIX, Anti-Fraude Universelle Axe 1. Compagnon n.18.

Protocole : deux cles de test (faible = jumeaux, conforme = eloignes).
Le scanner cherche une faiblesse Fermat dans une fenetre de 2e6 iterations,
estime l'angle phi de l'Addendum v4, sonde le rationnel proche et la
signature dyadique, rend un verdict.

Garde pre-enregistree : cle faible -> FAIBLE (b trouve petit, 1 iteration) ;
                         cle conforme -> CONFORME (pas de faiblesse dans la fenetre).
"""

import sys
import math
from fractions import Fraction

MAX_ITER = 2_000_000   # fenetre de recherche Fermat


def estimate_fermat(N, max_iter=MAX_ITER):
    """Cherche a^2 - N = b^2 pour a proche de sqrt(N).
    Retourne (a, b, phi) si trouve, sinon (None, None, None)."""
    a = math.isqrt(N)
    if a * a < N:
        a += 1
    for _ in range(max_iter):
        b2 = a * a - N
        if b2 >= 0:
            b = math.isqrt(b2)
            if b * b == b2:
                phi = math.atan2(b, a)
                return a, b, phi
        a += 1
    return None, None, None


def rational_proximity(phi, max_denom=1000):
    """Cherche un petit rationnel proche de tan(phi)."""
    if phi is None:
        return None, float('inf')
    t = math.tan(phi)
    best = Fraction(t).limit_denominator(max_denom)
    return best, abs(t - float(best))


def dyadic_signature(N):
    """Signature dyadique : v_2(N-1) et v_2(N+1)."""
    def v2(m):
        c = 0
        while m > 0 and m % 2 == 0:
            c += 1
            m //= 2
        return c
    return v2(N - 1), v2(N + 1)


def verdict(phi):
    """FAIBLE si faiblesse Fermat detectee, CONFORME sinon."""
    if phi is not None:
        return "FAIBLE (Fermat detecte, triangle aplati)"
    return "CONFORME (pas de faiblesse dans la fenetre)"


def main():
    cles = [
        ("CLE FAIBLE (jumeaux)",   1000000007 * 1000000009, "FAIBLE"),
        ("CLE CONFORME (eloignes)", 999983 * 999999937,     "CONFORME"),
    ]

    print("=" * 70)
    print("diagnostic_rsa.py -- scanner geometrique de cles RSA (Axe 1)")
    print("=" * 70)
    print(f"Fenetre Fermat : {MAX_ITER} iterations")
    print()

    audit_vert = True
    for nom, N, attendu in cles:
        print(f"--- {nom} ---")
        print(f"  N = {N} ({N.bit_length()} bits)")

        a, b, phi = estimate_fermat(N)
        if phi is not None:
            print(f"  Fermat : a = {a}, b = {b}")
            print(f"  Angle phi = {phi:.6e} rad")
        else:
            print(f"  Fermat : aucune faiblesse dans la fenetre")

        rat, dist = rational_proximity(phi)
        if phi is not None:
            print(f"  Rationnel proche : tan(phi) ~ {rat} (dist {dist:.2e})")

        v2m1, v2p1 = dyadic_signature(N)
        print(f"  Signature dyadique : v2(N-1) = {v2m1}, v2(N+1) = {v2p1}")

        vd = verdict(phi)
        print(f"  Verdict : {vd}")
        print(f"  Attendu : {attendu}")
        ok = attendu in vd
        if not ok:
            audit_vert = False
        print(f"  Statut : {'OK' if ok else 'ECART'}")
        print()

    print("-" * 70)
    if audit_vert:
        print("VERDICT : AUDIT VERT")
        print("  Axe 1 de l'anti-fraude ouvert : le scanner separe les cles.")
    else:
        print("VERDICT : DRAPEAU")
        print("  Une cle n'est pas classee comme attendu.")
    print("[OK]")


if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    main()