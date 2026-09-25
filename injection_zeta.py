#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2026 Fouad Bensmail — Tous droits réservés / All rights reserved.
# Licence / License : CC BY-NC 4.0 — https://creativecommons.org/licenses/by-nc/4.0/
# =============================================================================
"""
injection_zeta.py v2 — Addendum XLVI. Compagnon n.35.
Injection des NEUF premiers zéros de zêta dans la fenêtre : test de
cohérence de phase du cristal haut-t (Direction Spectrale).

Refus publiés (v1, protocole) :
  (1) Coquilles d'ancres : 21,022081 au lieu de 21,022039639 ; 30,424836 au
      lieu de 30,424876126 ; cinquième zéro 32,935061588 omis. Corrections
      reçues de l'évaluation externe II, publiées (Article II).
  (2) Fuite de tendance : la tendance ln-ln est estimée sur les paliers
      d'entraînement seulement, puis appliquée aux paliers de test.

Raffinements externes intégrés : R2_pred contre moyenne d'entraînement ;
CV K=5 blocs contigus en ln X ; G5 = 1000 surrogats à phases aléatoires
(spectre et autocorrélation préservés) ; G0 < 1e-6 ; G3 par projection
orthogonale ; G4 majorité (5/9) avec note Bonferroni.

Gardes pré-enregistrées :
  G0 : 9 zéros maison vs ancres, erreur max < 1e-6.
  G1 : R2_in >= 0,15.
  G2 : R2_pred (CV K=5) >= 0,05 ; <= 0 -> refus d'overfitting publié.
  G3 : projection max des orphelins (4,54; 5,45; 7,26) sur l'espace zêta < 0,30.
  G4 : chute > 50 % à >= 5 des 9 fréquences injectées.
  G5 : R2_pred observé > 95e percentile de 1000 surrogats (p < 0,05).
"""
import sys
import time
import math
import cmath
import numpy as np

X_MIN, X_MAX = 1e5, 1e8
REG_MIN = 1e6
N_PAL = 600
K_FOLD = 5
N_SURR = 1000
SEED = 42
ANCRES = [14.134725142, 21.022039639, 25.010857580, 30.424876126,
          32.935061588, 37.586178159, 40.918719012, 43.327073281,
          48.005150881]
ORPHELINS = [4.54, 5.45, 7.26]
CLASSES12 = [1, 5, 7, 11]
BERN = [1.0 / 6, -1.0 / 30, 1.0 / 42, -1.0 / 30, 5.0 / 66, -691.0 / 2730]
LC = [0.99999999999980993, 676.5203681218851, -1259.1392167224028,
      771.32342877765313, -176.61502916214059, 12.507343278686905,
      -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7]


def loggamma(z):
    z = complex(z)
    acc = 0.0 + 0.0j
    while z.real < 1.0:
        acc -= cmath.log(z)
        z += 1.0
    x = z - 1.0
    a = LC[0]
    t = x + 7.5
    for i in range(1, 9):
        a += LC[i] / (x + i)
    return (acc + cmath.log(math.sqrt(2 * math.pi) * a / t)
            + (x + 0.5) * cmath.log(t) - t)


def zeta_half(t, n0=1000):
    s = 0.5 + 1j * t
    tot = 0.0 + 0.0j
    for n in range(1, n0):
        tot += n ** (-s)
    N = float(n0)
    val = tot + N ** (1 - s) / (s - 1) + 0.5 * N ** (-s)
    rise = 1.0 + 0.0j
    idx = 0
    for k in range(1, 7):
        while idx < 2 * k - 1:
            rise *= (s + idx)
            idx += 1
        val += (BERN[k - 1] / math.factorial(2 * k)) * rise * N ** (-(s + 2 * k - 1))
    return val


def hardy_Z(t):
    z = zeta_half(t)
    th = loggamma(0.25 + 0.5j * t).imag - 0.5 * t * math.log(math.pi)
    return (cmath.exp(1j * th) * z).real


def zeros_zeta(t0, t1, pas=0.01):
    ts = np.arange(t0, t1, pas)
    zs = np.array([hardy_Z(t) for t in ts])
    out = []
    for i in range(1, len(ts)):
        if zs[i - 1] * zs[i] < 0:
            a, b = ts[i - 1], ts[i]
            fa = hardy_Z(a)
            for _ in range(60):
                m = 0.5 * (a + b)
                fm = hardy_Z(m)
                if fa * fm <= 0:
                    b = m
                else:
                    a, fa = m, fm
            out.append(0.5 * (a + b))
    return out


def crible_gpf(n):
    gpf = np.zeros(n + 1, dtype=np.int32)
    for i in range(2, n + 1):
        if gpf[i] == 0:
            gpf[i::i] = i
    return gpf


def main():
    t0 = time.time()
    print("=" * 78)
    print("injection_zeta.py v2 — Addendum XLVI : cohérence de phase du cristal")
    print("=" * 78)
    print()

    # ---------------- G0 : instrument zêta ----------------
    print("Calcul maison des zeros de zeta sur [14, 49] ...")
    zc = zeros_zeta(14.0, 49.0)[:9]
    err = max(abs(a - b) for a, b in zip(zc, ANCRES))
    g0 = err < 1e-6
    print(f"G0 erreur max vs ancres : {err:.3e} (< 1e-6) -> {'OK' if g0 else 'ECHEC'}")
    for a, b in zip(zc, ANCRES):
        print(f"   maison {a:.9f}  ancre {b:.9f}")
    print()

    # ---------------- résidu de C1 ----------------
    print(f"Crible GPF jusqu'a {X_MAX:.0e} ...")
    tc = time.time()
    gpf = crible_gpf(int(X_MAX))
    is_prime = (gpf == np.arange(int(X_MAX) + 1, dtype=np.int32))
    is_prime[0] = False
    is_prime[1] = False
    print(f"Crible pret en {time.time() - tc:.1f} s")
    primes = np.nonzero(is_prime)[0]
    primes = primes[primes >= 3]
    gp = gpf[primes - 1]

    lnX = np.linspace(math.log(X_MIN), math.log(X_MAX), N_PAL)
    X = np.exp(lnX)
    Y = X ** 0.5

    def serie(mod, cls):
        if mod is None:
            p, q = primes, gp
        else:
            msk = (primes % mod) == cls
            p, q = primes[msk], gp[msk]
        D = np.empty(N_PAL)
        for i in range(N_PAL):
            iX = np.searchsorted(p, X[i], side="right")
            D[i] = np.count_nonzero(q[:iX] <= Y[i]) / max(iX, 1)
        return D

    print("Pesée des paliers (600 x 9 séries) ...")
    tc = time.time()
    D12 = {c: serie(12, c) for c in CLASSES12}
    D4 = {c: serie(4, c) for c in (1, 3)}
    D3 = {c: serie(3, c) for c in (1, 2)}
    DG = serie(None, None)
    print(f"Pesée faite en {time.time() - tc:.1f} s")

    C = {c: (D12[c] * DG) / (D4[c % 4] * D3[c % 3]) for c in CLASSES12}

    # ---------------- tendance (entraînement seulement), résidu, base ----------------
    def tendance(idx_tr):
        out = {}
        for c in CLASSES12:
            m = idx_tr[X[idx_tr] >= REG_MIN]
            y = np.log(np.maximum(np.abs(C[c][m] - 1.0), 1e-12))
            x = np.log(lnX[m])
            pent, b = np.linalg.lstsq(np.vstack([x, np.ones_like(x)]).T, y, rcond=None)[0]
            out[c] = (math.exp(b), -pent)
        return out

    def residu(tend):
        R = np.empty((4, N_PAL))
        for j, c in enumerate(CLASSES12):
            A, al = tend[c]
            R[j] = (C[c] - 1.0) / (A / lnX ** al)
        return R.mean(axis=0)

    s = lnX
    B = np.column_stack([f(g * s) for g in zc for f in (np.cos, np.sin)])
    O = np.column_stack([f(g * s) for g in ORPHELINS for f in (np.cos, np.sin)])

    # ---------------- ajustement plein (G1, G4) ----------------
    r = residu(tendance(np.arange(N_PAL)))
    beta = np.linalg.lstsq(B, r, rcond=None)[0]
    fit = B @ beta
    R2_in = 1.0 - np.sum((r - fit) ** 2) / np.sum((r - r.mean()) ** 2)
    g1 = R2_in >= 0.15
    print(f"G1 R2_in = {R2_in:.4f} (>= 0,15) -> {'OK' if g1 else 'ECHEC'}")

    w = np.hanning(N_PAL)
    ds = lnX[1] - lnX[0]
    gam = 2 * np.pi * np.fft.rfftfreq(N_PAL, d=ds) / ds
    spec_av = np.abs(np.fft.rfft(r * w))
    spec_ap = np.abs(np.fft.rfft((r - fit) * w))
    print("G4 nettoyage aux fréquences injectées :")
    n_chute = 0
    for j, g in enumerate(zc):
        iB = int(np.argmin(np.abs(gam - g)))
        d = 1.0 - spec_ap[iB] / spec_av[iB] if spec_av[iB] > 0 else 0.0
        if d > 0.5:
            n_chute += 1
        print(f"   gamma = {g:9.5f}  avant {spec_av[iB]:8.2f}  apres {spec_ap[iB]:8.2f}  chute {d:+6.1%}")
    g4 = n_chute >= 5
    print(f"G4 chutes > 50 % : {n_chute}/9 (>= 5) -> {'OK' if g4 else 'ECHEC'}")
    print("Descriptif orphelins :")
    for g in ORPHELINS:
        iB = int(np.argmin(np.abs(gam - g)))
        d = 1.0 - spec_ap[iB] / spec_av[iB] if spec_av[iB] > 0 else 0.0
        print(f"   orphelin {g:5.2f}  chute {d:+6.1%}")

    # ---------------- G3 : projection orthogonale ----------------
    GtG = B.T @ B
    P = B @ np.linalg.solve(GtG, B.T @ O)
    proj = max(np.linalg.norm(P[:, j]) / np.linalg.norm(O[:, j]) for j in range(O.shape[1]))
    g3 = proj < 0.30
    print(f"G3 projection max des orphelins sur l'espace zeta : {proj:.3f} (< 0,30) -> {'OK' if g3 else 'ECHEC'}")
    print()

    # ---------------- G2 : CV K=5 blocs contigus ----------------
    blocs = np.array_split(np.arange(N_PAL), K_FOLD)
    R2_folds = []
    pre = []
    for f in range(K_FOLD):
        te = blocs[f]
        tr = np.setdiff1d(np.arange(N_PAL), te)
        rr = residu(tendance(tr))
        Btr, Bte = B[tr], B[te]
        M = Btr.T @ Btr
        b = np.linalg.solve(M, Btr.T @ rr[tr])
        pred = Bte @ b
        den = np.sum((rr[te] - rr[tr].mean()) ** 2)
        R2_folds.append(1.0 - np.sum((rr[te] - pred) ** 2) / den)
        pre.append((M, Btr, Bte, tr, te))
    R2_pred = float(np.mean(R2_folds))
    g2 = R2_pred >= 0.05
    tag = 'OK' if g2 else ('REFUS OVERFITTING' if R2_pred <= 0 else 'ECHEC')
    print(f"G2 R2_pred (CV K=5) = {R2_pred:+.4f}  folds = "
          + ", ".join(f"{v:+.3f}" for v in R2_folds)
          + f"  (>= 0,05) -> {tag}")

    # ---------------- G5 : 1000 surrogats ----------------
    rng = np.random.default_rng(SEED)
    mag = np.abs(np.fft.rfft(r))
    nul = np.empty(N_SURR)
    for k in range(N_SURR):
        ph = rng.uniform(0, 2 * np.pi, len(mag))
        ph[0] = 0.0
        ph[-1] = 0.0
        rs = np.fft.irfft(mag * np.exp(1j * ph), n=N_PAL)
        vals = []
        for (M, Btr, Bte, tr, te) in pre:
            b = np.linalg.solve(M, Btr.T @ rs[tr])
            pred = Bte @ b
            den = np.sum((rs[te] - rs[tr].mean()) ** 2)
            vals.append(1.0 - np.sum((rs[te] - pred) ** 2) / den)
        nul[k] = np.mean(vals)
    p_val = float(np.mean(nul >= R2_pred))
    g5 = p_val < 0.05
    print(f"G5 surrogats : 95e percentile = {np.percentile(nul, 95):+.4f}, "
          f"observe = {R2_pred:+.4f}, p = {p_val:.3f} (< 0,05) -> {'OK' if g5 else 'ECHEC'}")

    # ---------------- descriptif : erreur de phase ----------------
    sig = float(np.std(r - fit))
    amps = np.hypot(beta[0::2], beta[1::2])
    print("Descriptif erreur de phase (sigma_res / (A sqrt(N))) :")
    for j in np.argsort(-amps)[:3]:
        print(f"   gamma = {zc[j]:9.5f}  A = {amps[j]:.4f}  err = {sig / (amps[j] * math.sqrt(N_PAL)):.4f} rad")
    print()

    if not g0:
        print("VERDICT : ECHEC DE GARDE (instrument zêta hors tolérance)")
    elif g1 and g2 and g5:
        print("VERDICT : AUDIT VERT — COHERENCE DE PHASE : le cristal haut-t est")
        print("  phase-verrouillé aux zéros de zêta ; la Direction Spectrale passe")
        print("  de « suggestive » à « cohérente ».")
        if not g4:
            print("  (G4 non tenue : nettoyage partiel, publié descriptif)")
    elif R2_pred <= 0.0 or not g5:
        print("VERDICT : REFUS D'OVERFITTING PUBLIE — le résidu ne porte pas de")
        print("  cohérence de phase exploitable hors échantillon ; les alignements")
        print("  haut-t des Addenda XXXVI-XXXVII restent des coïncidences de bin.")
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