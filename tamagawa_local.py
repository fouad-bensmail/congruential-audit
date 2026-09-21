#!/usr/bin/env python3

# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# Non-commercial use only. Commercial use prohibited without written consent.
# =============================================================================
"""
tamagawa_local.py — troisième compagnon de la Conjecture du Cadre
(Remarque 5.3) : volumes locaux de Tamagawa du motif jumeau et indépendance
CRT mesurée (le global est le produit des locaux).

Trois pesées :
  1. volumes locaux : beta_p = (1-nu_p/p)/(1-1/p)^2 par comptage de residues ;
     produits partiels S(P) à P = 1e3..1e6 -> 1.3203171 (garde 1e-5) ;
  2. CRT mesuré : pour des ensembles de premiers de produit D <= 1e5, le
     comptage brut des survivants sur une période vaut prod (p-nu_p), et la
     fréquence sur n <= X colle au produit des fréquences locales à D/X près ;
  3. table locale : fractions exactes V_p = (p-nu_p)/p, mu_p = ((p-1)/p)^2,
     beta_p = V_p/mu_p pour p = 2,3,5,7,11.
Usage : python -u tamagawa_local.py [X] (défaut 10000000)
"""
import sys, math, time
from fractions import Fraction
import hunt_log

H = (0, 2)

def primes_to(n):
    c = bytearray([1])*(n+1); c[0:2] = b"\x00\x00"
    for i in range(2, int(n**0.5)+1):
        if c[i]:
            c[i*i:n+1:i] = bytearray(len(range(i*i, n+1, i)))
    return [i for i in range(2, n+1) if c[i]]

def nu_p(p):
    return len({h % p for h in H})

def period_count(D, plist):
    forb = {p: {h % p for h in H} for p in plist}
    per = 0
    for n in range(D):
        if all((n % p) not in forb[p] for p in plist):
            per += 1
    return per

def main():
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000_000
    t0 = time.time()
    print("[1/3] volumes locaux et produits partiels ...")
    ps = primes_to(1_000_000)
    for P in (1_000, 10_000, 100_000, 1_000_000):
        s = 1.0 # remise a zero a chaque palier (le bug etait la)
        for p in ps:
            if p > P: break
            s *= (1.0 - nu_p(p)/p) / (1.0 - 1.0/p)**2
        print(f" S({P:>7}) = {s:.7f}")
    garde = abs(s - 1.3203236) # 2*C2 = 1.32032363169...
    print(f" garde |S(1e6)-1.3203236| = {garde:.2e}")

    print("[2/3] indépendance CRT mesurée (global = produit des locaux) ...")
    SETS = [(2, 3), (2, 3, 5), (3, 5, 7), (2, 3, 5, 7), (5, 7, 11),
            (7, 11, 13), (2, 3, 5, 7, 11), (11, 13, 17, 19)]
    Dmax = max(math.prod(st) for st in SETS)
    worst = 0.0
    for st in SETS:
        D = math.prod(st); plist = list(st)
        per = period_count(D, plist)
        prod = 1
        for p in plist: prod *= (p - nu_p(p))
        cnt = (X // D) * per + period_count(X % D, plist)
        r = (cnt / X) / (per / D)
        worst = max(worst, abs(r - 1.0))
        print(f" D={D:>6} : periode==prod(p-nu) {per == prod} ; "
              f"freq X / produit locaux = {r:.6f}")
    print(f" déviation max = {worst:.2e} (borne ~ Dmax/X = {Dmax/X:.1e})")
    print("[3/3] table locale (fractions exactes) :")
    for p in (2, 3, 5, 7, 11):
        V = Fraction(p - nu_p(p), p)
        mu = Fraction(p - 1, p) ** 2
        print(f" p={p:2d} : V_p = {V} , mu_p = {mu} , "
              f"beta_p = {float(V/mu):.6f}")
    ok = garde < 1e-5 and worst < 3 * Dmax / X
    print(f"[verdict] tamagawa local : {'VERT' if ok else 'REFUSE'}")
    print(f"[OK] {time.time()-t0:.1f} s")
    hunt_log.log_scan("tamagawa-local", 3 if ok else 0, 0 if ok else 1,
                      scanner="tamagawa_local",
                      notes=f"X:{X} garde:{garde:.1e} crt-worst:{worst:.1e}")

if __name__ == "__main__":
    main()
