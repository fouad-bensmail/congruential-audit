#!/usr/bin/env python3

# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# Non-commercial use only. Commercial use prohibited without written consent.
# =============================================================================
"""
obstruction_modM.py — l'obstruction congruentielle a module quelconque.

Generalise obstruction_mod12.py : pese la lissite de p-1 (regle validee
P+(m) <= m^(1/u), u = 2..5) selon p mod M, pour tout module M >= 3.

Usage :
    python -u obstruction_modM.py 24
    python -u obstruction_modM.py 30
    python -u obstruction_modM.py 60
    python -u obstruction_modM.py 64

Gardes annoncees a l'avance :
  [0] Volumes forces : E[v_q(p-1) | classe] = plancher force + queue
      geometrique 1/(q-1) si a = 1 mod q^k, valuation exacte sinon.
      Garde : |z| < 4 par (classe, q).
  [1] Marges signees contre l'etalon global (classes unites poolees),
      aux deux echelles 10^6 et 10^7, budget sigma (* = < 25 lisses).
  [2] Ordre : le diviseur force d(a) = prod_q q^{E[v_q]} doit classer
      les classes. Garde : Spearman(d, marge u=2) > 0.7.
  [3] Jumeaux : classes de meme vecteur force -> marges indifferents,
      |z| < 3.5. Un ecart significatif signerait une structure AU-DELA
      des volumes forces (decouverte potentielle, a publier comme telle).
  [4] Persistance : Spearman des marges u=2 entre echelles. Garde : > 0.9.
"""
import math
import sys
import time
from array import array

import hunt_log

US = (2, 3, 4, 5)
SCALES = (1_000_000, 10_000_000)


def primes_to(n):
    c = bytearray([1]) * (n + 1)
    c[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if c[i]:
            c[i * i::i] = bytearray(len(range(i * i, n + 1, i)))
    return [i for i in range(2, n + 1) if c[i]]


def gpf_sieve(X):
    """gpf[m] = P+(m) (plus grand facteur premier), par ecrasement ascendant."""
    gpf = array('I', [0]) * (X + 1)
    for p in range(2, X + 1):
        if gpf[p] == 0:
            gpf[p::p] = array('I', [p]) * len(range(p, X + 1, p))
    return gpf


def v_q(n, q):
    v = 0
    while n % q == 0:
        n //= q
        v += 1
    return v


def factorize(M):
    qs = {}
    m = M
    d = 2
    while d * d <= m:
        if m % d == 0:
            k = 0
            while m % d == 0:
                m //= d
                k += 1
            qs[d] = k
        d += 1
    if m > 1:
        qs[m] = 1
    return qs


def forced_volumes(qs, units):
    """pred[a][q] = E[v_q(p-1) | p = a mod M]."""
    pred = {}
    for a in units:
        row = {}
        for q, k in qs.items():
            r = (a - 1) % q ** k
            if r == 0:
                row[q] = k + 1.0 / (q - 1)   # plancher k + queue geometrique
            else:
                row[q] = float(v_q(r, q))    # exactement determine
        pred[a] = row
    return pred


def forced_divisor(pred_a, qs):
    return math.exp(sum(pred_a[q] * math.log(q) for q in qs))


def weigh_scale(X, M, qs, units):
    ps = primes_to(X)
    gpf = gpf_sieve(X)
    cls = {a: {'n': 0,
               's': {u: 0 for u in US},
               'v': {q: 0 for q in qs},
               'w': {q: 0 for q in qs}} for a in units}
    glob = {'n': 0, 's': {u: 0 for u in US}}
    for p in ps:
        if math.gcd(p, M) != 1:
            continue
        a = p % M
        m = p - 1
        b = cls[a]
        b['n'] += 1
        glob['n'] += 1
        g = gpf[m]
        for u in US:
            if g <= m ** (1.0 / u):
                b['s'][u] += 1
                glob['s'][u] += 1
        for q in qs:
            mm = m
            v = 0
            while mm % q == 0:
                mm //= q
                v += 1
            b['v'][q] += v
            b['w'][q] += v * v
    return cls, glob


def ranks(v):
    order = sorted(range(len(v)), key=lambda i: v[i])
    rk = [0.0] * len(v)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        moy = (i + j) / 2.0 + 1.0
        for t in range(i, j + 1):
            rk[order[t]] = moy
        i = j + 1
    return rk


def spearman(xs, ys):
    rx, ry = ranks(xs), ranks(ys)
    n = len(xs)
    mx = sum(rx) / n
    my = sum(ry) / n
    cov = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    sx = math.sqrt(sum((r - mx) ** 2 for r in rx))
    sy = math.sqrt(sum((r - my) ** 2 for r in ry))
    return cov / (sx * sy) if sx * sy > 0 else 0.0


def main():
    if len(sys.argv) < 2:
        print("usage : python -u obstruction_modM.py M   (ex. 24, 30, 60, 64)")
        sys.exit(1)
    M = int(sys.argv[1])
    if M < 3:
        print("M doit etre >= 3")
        sys.exit(1)

    t0 = time.time()
    qs = factorize(M)
    units = [a for a in range(1, M) if math.gcd(a, M) == 1]
    pred = forced_volumes(qs, units)
    dvol = {a: forced_divisor(pred[a], qs) for a in units}

    print("=" * 78)
    print(f"OBSTRUCTION MOD {M} — lissite de p-1 par classe unite")
    print(f"phi({M}) = {len(units)} classes ; premiers q | M : {sorted(qs)} ; "
          f"echelles {SCALES}")
    print("=" * 78)

    R = {}
    for X in SCALES:
        print(f"\npesee X = {X} ...")
        R[X] = weigh_scale(X, M, qs, units)

    drapeaux = 0
    Xb = SCALES[-1]

    # ---- [0/4] volumes forces --------------------------------------------
    cls, glob = R[Xb]
    print(f"\n[0/4] garde deterministe : volumes forces (X = {Xb})")
    print("      classe  " + "  ".join(f"E[v{q}] mes/pred (z)" for q in sorted(qs))
          + "   d force")
    for a in units:
        b = cls[a]
        if b['n'] == 0:
            continue
        cells = []
        for q in sorted(qs):
            mes = b['v'][q] / b['n']
            var = max(b['w'][q] / b['n'] - mes * mes, 0.0)
            se = math.sqrt(var / b['n']) if var > 0 else 0.0
            pr = pred[a][q]
            if se > 0:
                z = (mes - pr) / se
            else:
                z = 0.0 if abs(mes - pr) < 1e-9 else 999.0
            cells.append(f"{mes:.4f}/{pr:.4f} ({z:+.1f})")
            if abs(z) > 4:
                drapeaux += 1
        print(f"      c{a:<5} " + "  ".join(cells) + f"   {dvol[a]:.2f}")

    # ---- [1/4] marges ------------------------------------------------------
    for X in SCALES:
        cls, glob = R[X]
        gr = {u: glob['s'][u] / glob['n'] for u in US}
        print(f"\n[1/4] proportions et marges (X = {X}) — etalon global : "
              + "/".join(f"{gr[u]:.5f}" for u in US))
        print("      classe       n   " + "".join(f"rho(u={u})  " for u in US)
              + "marge2%(z)       marge5%(z)")
        for a in units:
            b = cls[a]
            if b['n'] == 0:
                continue
            rh = {u: b['s'][u] / b['n'] for u in US}
            row = f"      c{a:<5}{b['n']:>8}   " + "".join(f"{rh[u]:<10.5f}" for u in US)
            for u in (2, 5):
                g = gr[u]
                se = math.sqrt(g * (1 - g) / b['n'])
                z = (rh[u] - g) / se if se > 0 else 0.0
                mg = (rh[u] / g - 1) * 100
                star = "*" if b['s'][u] < 25 else " "
                row += f"{mg:>+8.2f}{star}({z:>+6.1f})   "
            print(row)

    # ---- [2/4] ordre --------------------------------------------------------
    cls, glob = R[Xb]
    g2 = glob['s'][2] / glob['n']
    liste = [a for a in units if cls[a]['n'] > 0]
    marg2 = {a: (cls[a]['s'][2] / cls[a]['n']) / g2 - 1 for a in liste}
    sp_ordre = spearman([dvol[a] for a in liste], [marg2[a] for a in liste])
    print(f"\n[2/4] ordre : diviseur force d(a) vs marge u=2 (X = {Xb})")
    top_d = sorted(liste, key=lambda a: -dvol[a])[:3]
    top_m = sorted(liste, key=lambda a: -marg2[a])[:3]
    bot_d = sorted(liste, key=lambda a: dvol[a])[:3]
    bot_m = sorted(liste, key=lambda a: marg2[a])[:3]
    print("      top predit (d) : " + ", ".join(f"c{a} ({dvol[a]:.1f})" for a in top_d))
    print("      top mesure (%) : " + ", ".join(f"c{a} ({marg2[a]*100:+.1f})" for a in top_m))
    print("      bas predit (d) : " + ", ".join(f"c{a} ({dvol[a]:.1f})" for a in bot_d))
    print("      bas mesure (%) : " + ", ".join(f"c{a} ({marg2[a]*100:+.1f})" for a in bot_m))
    print(f"      Spearman = {sp_ordre:.3f}  (garde : > 0.7)")
    if sp_ordre <= 0.7:
        drapeaux += 1

    # ---- [3/4] jumeaux -------------------------------------------------------
    print(f"\n[3/4] jumeaux : meme vecteur force -> marges indifferents (u=2, X = {Xb})")
    groupes = {}
    for a in liste:
        key = tuple(pred[a][q] for q in sorted(qs))
        groupes.setdefault(key, []).append(a)
    n_tests = 0
    for key, membres in sorted(groupes.items(), key=lambda kv: -len(kv[1])):
        if len(membres) < 2:
            continue
        ns = [cls[a]['n'] for a in membres]
        ss = [cls[a]['s'][2] for a in membres]
        gm = sum(ss) / sum(ns)
        zmax = 0.0
        amax = membres[0]
        for a, n_a, s_a in zip(membres, ns, ss):
            r = s_a / n_a
            se = math.sqrt(gm * (1 - gm) / n_a)
            z = abs(r - gm) / se if se > 0 else 0.0
            if z > zmax:
                zmax, amax = z, a
        n_tests += len(membres)
        etat = "VERT" if zmax < 3.5 else "STRUCTURE AU-DELA DES VOLUMES"
        if zmax >= 3.5:
            drapeaux += 1
        noms = ", ".join(f"c{a}" for a in membres)
        print(f"      [{noms}] : z_max = {zmax:.2f} (c{amax}) -> {etat}")
    if n_tests == 0:
        print("      (aucune famille de jumeaux pour ce module)")

    # ---- [4/4] persistance ---------------------------------------------------
    c6, g6 = R[SCALES[0]]
    c7, g7 = R[SCALES[1]]
    m6 = [(c6[a]['s'][2] / c6[a]['n']) / (g6['s'][2] / g6['n']) for a in liste]
    m7 = [(c7[a]['s'][2] / c7[a]['n']) / (g7['s'][2] / g7['n']) for a in liste]
    sp_pers = spearman(m6, m7)
    print(f"\n[4/4] persistance : Spearman(marges u=2, 10^6 vs 10^7) = {sp_pers:.4f}"
          f"   (garde : > 0.9)")
    if sp_pers <= 0.9:
        drapeaux += 1

    verdict = ("AUDIT VERT : toutes les gardes tiennent" if drapeaux == 0
               else f"{drapeaux} DRAPEAU(X) : voir sections ci-dessus")
    print("\n" + "=" * 78)
    print(f"VERDICT mod {M} : {verdict}")
    print("=" * 78)
    print(f"[OK] {time.time()-t0:.1f} s")

    hunt_log.log_scan(f"obstruction-mod{M}", 5, drapeaux,
                      scanner="obstruction_modM",
                      notes=(f"M={M} phi={len(units)} ordre={sp_ordre:.2f} "
                             f"persistance={sp_pers:.3f} drapeaux={drapeaux}"))


if __name__ == "__main__":
    main()