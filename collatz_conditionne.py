#!/usr/bin/env python3

# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# Non-commercial use only. Commercial use prohibited without written consent.
# =============================================================================
"""
collatz_conditionne.py — le biais des pas impairs de Collatz, conditionne mod 12.

Hypothese du cadre : le biais des pas impairs dans les trajectoires de Collatz,
decompose par classe de n mod 12, suit les volumes locaux 2x3 (les memes qui
gouvernent la lissite de p-1).

Garde null [0] : la fraction globale de pas impairs tend vers 1/3 (chaque pas
impair est suivi en moyenne de 2 divisions par 2, loi geometrique de v2(3n+1)).

Gardes :
  [0] fraction globale proche de 1/3 aux deux echelles ;
  [1] decomposition mod 12 : table des fractions par classe ;
  [2] signature 2x3 : les classes a fort volume 2 ou 3 se distinguent ;
  [3] persistance entre 10^5 et 5x10^5 (structure vs fluctuation).

Usage : python -u collatz_conditionne.py
Note : si la memoire tire la langue, reduisez X2 dans SCALES.
"""
import math, time
import hunt_log

SCALES = (100_000, 500_000)
MOD = 12
NULL = 1.0 / 3.0

def weigh_collatz(X1, X2):
    # memo[v] = (pas_impairs, pas_pairs) pour aller de v jusqu'a 1.
    # On ne memorise que v <= X2 pour borner la memoire ; au-dela, on recalcule.
    memo = {1: (0, 0)}
    cls_odd = [0] * MOD
    cls_tot = [0] * MOD
    cls_cnt = [0] * MOD
    snaps = {}
    for n in range(2, X2 + 1):
        path = []
        m = n
        while m not in memo:
            path.append(m)
            m = 3 * m + 1 if m & 1 else m >> 1
        o, e = memo[m]
        for v in reversed(path):
            if v & 1:
                o += 1
            else:
                e += 1
            if v <= X2:
                memo[v] = (o, e)
        o, e = memo[n]
        t = o + e
        r = n % MOD
        cls_odd[r] += o
        cls_tot[r] += t
        cls_cnt[r] += 1
        if n == X1:
            snaps[X1] = (cls_odd[:], cls_tot[:], cls_cnt[:])
    snaps[X2] = (cls_odd[:], cls_tot[:], cls_cnt[:])
    return snaps

def frac_stats(snap):
    cls_odd, cls_tot, cls_cnt = snap
    go, gt = sum(cls_odd), sum(cls_tot)
    return go, gt, go / gt, cls_odd, cls_tot, cls_cnt

def main():
    t0 = time.time()
    X1, X2 = SCALES
    snaps = weigh_collatz(X1, X2)

    print("[0/3] garde null : fraction globale de pas impairs (attendu ~1/3) ...")
    gdev = {}
    for X in SCALES:
        go, gt, gf, *_ = frac_stats(snaps[X])
        dev = gf - NULL
        gdev[X] = dev
        print(f"      X={X:>7} : frac = {gf:.5f} ; ecart a 1/3 = {dev:+.5f} "
              f"({dev/NULL*100:+.3f} % relatif)")

    print("[1/3] decomposition mod 12 (fraction ponderee par pas) ...")
    for X in SCALES:
        _, _, _, cls_odd, cls_tot, cls_cnt = frac_stats(snaps[X])
        print(f"      X = {X} :")
        print(f"      {'classe':<7}{'n':>9}{'frac':>10}{'ecart':>12}{'exces%':>9}")
        for r in range(MOD):
            if cls_tot[r] == 0:
                continue
            f = cls_odd[r] / cls_tot[r]
            dev = f - NULL
            print(f"      c{r:<6}{cls_cnt[r]:>9}{f:>10.5f}{dev:>+12.5f}{dev/NULL*100:>+9.3f}")

    print("[2/3] signature 2x3 : les quatre classes les plus deviees (X max) ...")
    _, _, _, cls_odd, cls_tot, cls_cnt = frac_stats(snaps[X2])
    devs = []
    for r in range(MOD):
        if cls_tot[r]:
            f = cls_odd[r] / cls_tot[r]
            devs.append((abs(f - NULL), r, f))
    devs.sort(reverse=True)
    for ad, r, f in devs[:4]:
        print(f"      c{r:<3} frac = {f:.5f} ; ecart = {f-NULL:+.5f}")

    print("[3/3] persistance : ecart global et classement entre echelles ...")
    contr = gdev[X1] / gdev[X2] if gdev[X2] != 0 else float('inf')
    print(f"      ecart global : X1 {gdev[X1]:+.5f} -> X2 {gdev[X2]:+.5f} "
          f"(ratio {contr:.2f})")
    _, _, _, o1, t1, _ = frac_stats(snaps[X1])
    _, _, _, o2, t2, _ = frac_stats(snaps[X2])
    d1 = [(o1[r]/t1[r] - NULL) if t1[r] else 0.0 for r in range(MOD)]
    d2 = [(o2[r]/t2[r] - NULL) if t2[r] else 0.0 for r in range(MOD)]
    m1 = sum(d1) / MOD
    m2 = sum(d2) / MOD
    cov = sum((d1[r]-m1) * (d2[r]-m2) for r in range(MOD))
    s1 = math.sqrt(sum((d1[r]-m1)**2 for r in range(MOD)))
    s2 = math.sqrt(sum((d2[r]-m2)**2 for r in range(MOD)))
    corr = cov / (s1*s2) if s1*s2 > 0 else 0.0
    print(f"      correlation des ecarts par classe entre echelles : {corr:.3f}")

    print(f"\n[OK] {time.time()-t0:.1f} s")
    hunt_log.log_scan("collatz-conditionne", 3, 0,
                      scanner="collatz_conditionne",
                      notes=f"global_dev:{gdev[X2]:+.5f} corr:{corr:.2f}")

if __name__ == "__main__":
    main()