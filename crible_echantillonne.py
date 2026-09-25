#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# Utilisation commerciale interdite sans autorisation écrite de l'auteur.
# Non-commercial use only. Commercial use prohibited without written consent.
# =============================================================================
"""
crible_echantillonne.py — Addendum XXXIX. Compagnon n.28.
Le crible échantillonné : l'accès de Tang appliqué à l'obstruction,
et le test de rang à 10^8 et 10^9.

Inspiration publiée : E. Tang (STOC'19) — l'accès par échantillonnage
remplace l'accès complet. Ici : N_W fenêtres aléatoires de largeur W,
placées uniformément dans [2, X-W] ; chaque premier observé est pondéré
par 1/couverture, ce qui garde l'estimateur des proportions cumulées
SANS BIAIS, sans jamais porter la table GPF de [1, X] (4 Go à 10^9).

Question (test pré-enregistré de l'Addendum XXXVIII) : à 10^8, le ratio
RMS(R)/RMS(bruit) du rang 1 reste-t-il ~1,4 (covariance inter-modules
confirmée, cristal clos) ou monte-t-il au-dessus de 2,0 (STRUCTURE,
sigma_2 émerge) ? Et à 10^9 (exploration) ?

Protocole :
  - N_W fenêtres de largeur W, départs uniformes dans [2, X-W] (graine fixe).
  - Par fenêtre : crible décalé de primalité (premiers <= sqrt(X)) ; pour chaque
    premier p de la fenêtre, m = p-1 dépouillé des premiers <= X^(1/u) ;
    lisse ssi reste 1 (règle cumulative X^(1/u), Addendum XXXVIII).
  - Agrégation pondérée = estimateur sans biais des proportions cumulées à X.
  - Matrice L[(M,a), u] = ln(p(a,u,M)/p_glob(u)) ; SVD ; gardes.

Gardes pré-enregistrées :
  G1 (densité échantillonneur) : densité globale à 10^7 dans [0,40 ; 0,45]
     (ancre plein crible 0,4254, Addendum XXXVIII).
  G2 (cristal reproduit à 10^7) : fraction sigma_1 >= 0,90 ;
     |Pearson(u1, ln d)| >= 0,95 ; kappa(5)/kappa(2) dans [4,5 ; 7,0].
  G3 (test pré-enregistré à 10^8) : ratio <= 2,0 -> covariance confirmée ;
     > 2,0 -> STRUCTURE (sigma_2 émerge). Les deux issues sont publiées.
  G4 (exploration 10^9) : ratio, fraction sigma_1, kappa(u) rapportés, sans seuil.
"""
import sys
import time
import math
import numpy as np

MODULES = [12, 24, 60]
US = [2, 3, 4, 5]
N_W = 120
W = 10 ** 6
SEED = 20260923
TARGETS = [10 ** 7, 10 ** 8, 10 ** 9]


def primes_up_to(n):
    if n < 2:
        return np.array([], dtype=np.int64)
    is_p = np.ones(n + 1, dtype=bool)
    is_p[:2] = False
    for i in range(2, int(math.isqrt(n)) + 1):
        if is_p[i]:
            is_p[i * i::i] = False
    return np.nonzero(is_p)[0]


def forced_valuation(a, q, k):
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


def window_primes(start, w, sqrt_primes):
    seg = np.ones(w, dtype=bool)
    for q in sqrt_primes:
        first = (q - start % q) % q
        seg[first::q] = False
        if start <= q < start + w:
            seg[q - start] = True
    return start + np.nonzero(seg)[0]


def smooth_mask(pm1, y_primes):
    m_act = pm1.copy()
    act = m_act > 1
    for q in y_primes:
        if not act.any():
            break
        sub = m_act[act]
        div = (sub % q == 0)
        while div.any():
            sub[div] //= q
            div = (sub % q == 0)
        m_act[act] = sub
        act = m_act > 1
    return m_act == 1


def pearson(x, y):
    return float(np.corrcoef(np.asarray(x, float), np.asarray(y, float))[0, 1])


def rms(v):
    v = np.asarray(v, float).ravel()
    return float(np.sqrt(np.mean(v ** 2)))


def main():
    t0 = time.time()
    print("=" * 70)
    print("crible_echantillonne.py — Addendum XXXIX : le crible echantillonne")
    print("=" * 70)
    print(f"Fenetres : N_W = {N_W}, W = {W}, graine = {SEED}")
    print()

    rows = [(M, a, math.log(forced_divisor(a, M)))
            for M in MODULES for a in range(1, M) if math.gcd(a, M) == 1]
    n_rows = len(rows)
    g = np.array([r[2] for r in rows])
    idx_of = {(M, a): i for i, (M, a, _) in enumerate(rows)}

    results = {}
    for X in TARGETS:
        print(f"--- X = {X:.0e} ---")
        rng = np.random.default_rng(SEED + int(math.log10(X)))
        starts = rng.integers(2, X - W, size=N_W)
        sqrt_primes = primes_up_to(int(math.isqrt(X)) + 1)
        y_primes = {u: primes_up_to(int(X ** (1.0 / u)) + 1) for u in US}

        Sw = np.zeros(n_rows); Nw = np.zeros(n_rows); Nw2 = np.zeros(n_rows)
        Swu = {u: np.zeros(n_rows) for u in US}
        Sg = 0.0; Ng = 0.0
        Sgu = {u: 0.0 for u in US}

        for s in starts:
            pw = window_primes(s, W, sqrt_primes)
            pw = pw[(pw >= 3) & (pw <= X)]
            if len(pw) == 0:
                continue
            cov = np.minimum(pw, X - W) - np.maximum(2, pw - W + 1) + 1
            wgt = 1.0 / cov.astype(float)
            pm1 = pw - 1
            smooth = {u: smooth_mask(pm1, y_primes[u]) for u in US}
            clsM = {M: pw % M for M in MODULES}
            for (M, a), i in idx_of.items():
                msk = clsM[M] == a
                if not msk.any():
                    continue
                ww = wgt[msk]
                Nw[i] += ww.sum()
                Nw2[i] += np.sum(ww ** 2)
                for u in US:
                    Swu[u][i] += ww[smooth[u][msk]].sum()
            Ng += wgt.sum()
            for u in US:
                Sgu[u] += wgt[smooth[u]].sum()

        dens = {u: Sgu[u] / Ng for u in US}
        n_eff = Nw ** 2 / np.maximum(Nw2, 1e-12)
        P = np.zeros((n_rows, len(US)))
        Sig = np.zeros((n_rows, len(US)))
        for j, u in enumerate(US):
            p_col = Swu[u] / np.maximum(Nw, 1e-12)
            P[:, j] = p_col
            Sig[:, j] = np.sqrt((1.0 - p_col) / np.maximum(p_col * n_eff, 1e-12))
        L = np.log(P / dens[None, :].reshape(1, len(US))[:, 0][None, :] if False else P / np.array([dens[u] for u in US])[None, :])

        U, s, Vt = np.linalg.svd(L, full_matrices=False)
        frac = (s ** 2) / float(np.sum(s ** 2))
        u1 = U[:, 0]
        corr = pearson(u1, g)
        signe = 1.0 if corr >= 0 else -1.0
        u1 = u1 * signe
        kappa = s[0] * Vt[0, :] * signe
        kappa_n = kappa / kappa[0]
        R = L - np.outer(s[0] * U[:, 0], Vt[0, :])
        ratio = rms(R) / rms(Sig)

        print(f"  densite globale u=2 : {dens[2]:.4f} ; u=3 : {dens[3]:.4f}")
        print(f"  fraction sigma1 : {frac[0]:.4f} ; |Pearson(u1, ln d)| : {abs(corr):.4f}")
        print(f"  kappa(u) normalise : " +
              " ; ".join(f"u={u}: {k:.3f}" for u, k in zip(US, kappa_n)))
        print(f"  ratio residu/bruit : {ratio:.2f}")
        results[X] = dict(dens=dens, frac=frac[0], corr=abs(corr),
                          kappa=kappa_n, ratio=ratio)
        print()

    r7, r8, r9 = results[10**7], results[10**8], results[10**9]
    g1_ok = 0.40 <= r7["dens"][2] <= 0.45
    g2_ok = (r7["frac"] >= 0.90 and r7["corr"] >= 0.95
             and 4.5 <= r7["kappa"][3] / r7["kappa"][0] <= 7.0)
    print(f"G1 densite echantillonneur a 1e7 dans [0,40 ; 0,45] -> {'OK' if g1_ok else 'ECHEC'}")
    print(f"G2 cristal reproduit a 1e7 (fraction, Pearson, kappa) -> {'OK' if g2_ok else 'ECHEC'}")
    cov_ok = r8["ratio"] <= 2.0
    print(f"G3 test pre-enregistre a 1e8 : ratio = {r8['ratio']:.2f} -> "
          + ("COVARIANCE CONFIRMEE (cristal clos)" if cov_ok
             else "STRUCTURE (sigma2 emerge)"))
    print(f"G4 exploration 1e9 : ratio = {r9['ratio']:.2f}, "
          f"fraction sigma1 = {r9['frac']:.4f}, "
          f"kappa(5)/kappa(2) = {r9['kappa'][3] / r9['kappa'][0]:.3f}")
    print()
    if g1_ok and g2_ok:
        print("VERDICT : AUDIT VERT")
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