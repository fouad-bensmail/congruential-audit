#!/usr/bin/env python3
"""
microscope_haut.py — v3.4 — microscope spectral COMPLET (pur Python, sans dependance).

Histoire de la maison (tous les refus publies) :
  v3 (11 sept. 2026) : moyenne mobile a fenetres retrecies aux bords -> peigne
        d'interferences (41 pics sous gamma=100, beta=0.5967) ; garde N(T) refuse.
  v3.1 : detrendage polynomial degre 3 + taper de Hann -> 29 premiers zeros
        nommes, beta = 0.5031 +/- 0.0077, horizon ~101 (seuil global 4x mediane).
  v3.2 : seuil global sur spectre aplati (x gamma) -> cecite : 0 pic ; garde refuse.
  v3.3 : seuil 3.5x MOYENNE locale -> sur-correction : 5 pics (la moyenne locale
        est gonflee par les pics voisins) ; garde refuse (5 contre 29 a T=100).
        Mais les 5 pics s'appairent aux vrais zeros a <= 0.02 : appairage valide.
  v3.4 : seuil 4x MEDIANE locale (le plancher local), calculee sur sous-grille
        (pas 25 bins) puis interpolee : les pics ne gonflent pas leur propre seuil.

Mesures produites :
  1. pi(x) exact sur grille geometrique en u = log x (siege segmente, < 10 Mo) ;
  2. E = pi - li, poids ln(x)/sqrt(x), detrendage polynomial, taper de Hann ;
  3. scan Goertzel gamma in [10, GMAX] pas 0.1, seuil = 4x mediane locale ;
  4. garde N(T) (Riemann-von Mangoldt) : comptes contre attendus ;
  5. beta : amplitude de gamma_1 fenetre par fenetre (detrend lineaire + Hann),
     pente log-log -> beta = 1/2 + pente, avec erreur type ;
  6. appairage aux zeros connus (30 embarques, extensible via zeros_connus.txt) ;
  7. horizon : gamma apparie maximal, comptes apparies/nus.

Usage : python -u microscope_haut.py [X_MAX] [GAMMA_MAX] (defauts 1e8, 500)
"""
import sys, math, time, os
import hunt_log

SEG = 1 << 20
G1 = 14.134725147
CONNUS = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446241, 59.347044, 60.831718, 65.112544,
    67.079813, 69.546402, 72.067158, 75.704691, 77.144840,
    81.077313, 82.914541, 84.735496, 87.425275, 88.809111,
    92.491899, 94.651344, 95.870642, 98.831194, 101.317851,
]

def petits_premiers(z):
    c = bytearray([1]) * (z + 1); c[0:2] = b"\x00\x00"
    for i in range(2, int(z ** 0.5) + 1):
        if c[i]:
            c[i*i:z+1:i] = bytearray(len(range(i*i, z+1, i)))
    return [i for i in range(2, z + 1) if c[i]]

def li_asymp(x):
    L = math.log(x); s = 1.0; f = 1.0
    for k in range(1, 13):
        f *= k; s += f / L ** k
    return x / L * s

def detrend_poly(u, G, deg):
    m = deg + 1; n = len(u)
    A = [[0.0]*m for _ in range(m)]; b = [0.0]*m
    for i in range(n):
        ui, gi = u[i], G[i]; pu = 1.0
        for r in range(m):
            pc = 1.0; gr = gi * pu
            for c in range(m):
                A[r][c] += pu * pc; pc *= ui
            b[r] += gr; pu *= ui
    for r in range(m):
        p = max(range(r, m), key=lambda k: abs(A[k][r]))
        A[r], A[p] = A[p], A[r]; b[r], b[p] = b[p], b[r]
        d = A[r][r]
        for c in range(r, m): A[r][c] /= d
        b[r] /= d
        for k in range(m):
            if k != r and A[k][r]:
                f = A[k][r]
                for c in range(r, m): A[k][c] -= f * A[r][c]
                b[k] -= f * b[r]
    return [G[i] - sum(b[r] * u[i]**r for r in range(m)) for i in range(n)]

def hann(n):
    return [0.5 - 0.5 * math.cos(2*math.pi*k/(n-1)) for k in range(n)]

def goertzel(vals, du, gamma):
    w = 2.0 * math.cos(gamma * du); s1 = s2 = 0.0
    for v in vals:
        s0 = v + w * s1 - s2; s2 = s1; s1 = s0
    return math.sqrt(max(s1*s1 + s2*s2 - w*s1*s2, 0.0))

def main():
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000_000
    GMAX = float(sys.argv[2]) if len(sys.argv) > 2 else 500.0
    t0 = time.time(); du = 0.005
    u0, u1 = math.log(100.0), math.log(float(X))
    M = int((u1 - u0) / du)
    u = [u0 + k * du for k in range(M)]
    xs = [math.exp(v) for v in u]; ns = [int(v) for v in xs]

    print(f"[1/5] sieve segmente jusqu'a {X} (< 10 Mo) ...")
    rac = petits_premiers(int(X ** 0.5) + 1)
    pi_k = [0]*M; cum = 0; g = 0
    for a in range(2, X + 1, SEG):
        b = min(a + SEG - 1, X)
        seg = bytearray([1]) * (b - a + 1)
        for p in rac:
            if p * p > b: break
            st = ((a + p - 1) // p) * p
            if st == p: st += p
            seg[st-a:b-a+1:p] = bytearray(len(range(st, b + 1, p)))
        while g < M and ns[g] <= b:
            pi_k[g] = cum + seg[0:ns[g]-a+1].count(1); g += 1
        cum += seg.count(1)
    while g < M:
        pi_k[g] = cum; g += 1

    print("[2/5] E = pi - li, poids, detrend degre 3, Hann ...")
    G = [(pi_k[k] - li_asymp(xs[k])) * u[k] / math.sqrt(xs[k]) for k in range(M)]
    G = detrend_poly(u, G, 3)
    tap = hann(M)
    Gt = [G[k] * tap[k] for k in range(M)]

    print(f"[3/5] scan Goertzel jusqu'a gamma = {GMAX}, seuil 4x mediane locale ...")
    gam, mag = [], []
    gg = 10.0
    while gg <= GMAX:
        gam.append(gg); mag.append(goertzel(Gt, du, gg)); gg += 0.1

    # v3.4 : mediane locale sur sous-grille (le plancher, sans les pics), interpolee
    STEP = 25
    HW = 300 # demi-fenetre : +/- 30 en gamma
    meds = []
    for j in range(0, len(mag), STEP):
        a = max(0, j-HW); b = min(len(mag), j+HW+1)
        w = sorted(mag[a:b])
        meds.append(w[len(w)//2])
    def med_at(j):
        k = min(j // STEP, len(meds)-2)
        f = (j % STEP)/float(STEP)
        return meds[k]*(1.0-f) + meds[k+1]*f
    pics = []
    for j in range(1, len(mag)-1):
        if mag[j] > 4.0*med_at(j) and mag[j] >= mag[j-1] and mag[j] > mag[j+1]:
            den = mag[j-1] - 2*mag[j] + mag[j+1]
            d = 0.0 if den == 0 else 0.5*(mag[j-1]-mag[j+1])/den
            pics.append((gam[j] + 0.1*max(-1.0, min(1.0, d)), mag[j]))
    pics.sort()

    print(f"[4/5] garde N(T) : {len(pics)} pics")
    print(" T | pics <= T | N(T) attendu")
    for T in (50, 100, 150, 200, 300, 400, 500):
        if T <= GMAX:
            nt = (T/(2*math.pi))*(math.log(T/(2*math.pi)) - 1) + 7/8
            c = sum(1 for p, _ in pics if p <= T)
            print(f" {T:3d} | {c:3d} | {nt:7.2f}")

    us, ys = [], []
    e = 3
    while 10 ** (e + 1) <= X:
        ka = int((math.log(10**e) - u0)/du); kb = int((math.log(10**(e+1)) - u0)/du)
        if kb - ka > 100:
            uw = u[ka:kb]; gw = detrend_poly(uw, G[ka:kb], 1)
            tw = hann(len(gw))
            aw = goertzel([gw[i]*tw[i] for i in range(len(gw))], du, G1)
            if aw > 0:
                us.append(0.5*(math.log(10**e)+math.log(10**(e+1))))
                ys.append(math.log(aw * G1))
        e += 1
    n = len(us); mu = sum(us)/n; my = sum(ys)/n
    den = sum((v-mu)**2 for v in us)
    slo = sum((us[i]-mu)*(ys[i]-my) for i in range(n))/den
    res = [ys[i] - (my + slo*(us[i]-mu)) for i in range(n)]
    se = math.sqrt(sum(r*r for r in res)/(n-2)/den) if n > 2 else 0.0
    print(f"[5/5] beta = {0.5+slo:.4f} +/- {se:.4f} ({n} fenetres d'une decade)")

    known = sorted(set(CONNUS) | (
        {float(l) for l in open("zeros_connus.txt") if l.strip()}
        if os.path.exists("zeros_connus.txt") else set()))
    print(" detecte | connu proche | ecart | etat")
    npair = 0; horizon = 0.0
    for p, _ in pics[:40]:
        k = min(known, key=lambda z: abs(z - p))
        d = p - k
        etat = "apparie" if abs(d) <= 0.30 else "NU"
        if abs(d) <= 0.30:
            npair += 1; horizon = max(horizon, p)
        print(f" {p:8.4f} | {k:8.4f} | {d:+.4f} | {etat}")
    nnus = len(pics) - npair
    print(f"[horizon] gamma apparie maximal = {horizon:.2f} ; "
          f"{npair} apparies / {nnus} nus sur {len(pics)} pics")
    print(f"[OK] {time.time()-t0:.1f} s ; memoire : sieve segmente < 10 Mo.")
    hunt_log.log_scan("microscope-haut", len(pics), 0,
                      scanner="microscope_haut_v3.4",
                      notes=f"X:{X} beta:{0.5+slo:.4f}+/-{se:.4f} "
                            f"horizon:{horizon:.1f} apparies:{npair} nus:{nnus}")

if __name__ == "__main__":
    main()
